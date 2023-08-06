"""Code for setting up diffeqpy solvers."""

import time
import numpy as np
import math
ODE_SOLVER_METHOD_DEFAULT = 'TRBDF2'

from pvder.DER_wrapper import DERModel

from pvder.grid_components import Grid
from pvder.dynamic_simulation import DynamicSimulation
from pvder.simulation_events import SimulationEvents
from pvder.simulation_utilities import SimulationUtilities,SimulationResults
from pvder.logutil import LogUtil


from pvder import utility_functions


def setup_pyjulia(sysimage_path="/home/splathottam/images/sys.so"):
	"""Method to lazily setup PyJulia"""	
	
	from julia.api import LibJulia
	api = LibJulia.load()
	api.sysimage = sysimage_path #"/home/splathottam/images/sys.so"
	print("Loading system image from Julia:{}".format(api.sysimage))
	api.init_julia()

def import_diffeqpy(import_sundials = False,import_steadystate = False,set_blas_thread=False,n_blas_threads = 18):
	"""Method to lazily import diffeqpy"""
	
	diffeqpy_dict = {}
	
	tic = time.perf_counter()
	try:
		from julia import Base #Try if import succeeds
	except:
		setup_pyjulia(sysimage_path="/home/splathottam/images/sys.so")
		
	finally:
		
		print("Importing ode from diffeqpy...")
		from diffeqpy import ode #de #Only ode required
		diffeqpy_dict.update({'ode':ode})
		
		if import_sundials:
			print("Importing Sundials...")
			from julia import Sundials
			diffeqpy_dict.update({'Sundials':Sundials})
		if import_steadystate:
			print("Importing SteadyStateDiffEq...")
			from julia import SteadyStateDiffEq
			diffeqpy_dict.update({'SteadyStateDiffEq':SteadyStateDiffEq})
	
	if set_blas_thread:
		from julia import Main
		from julia import LinearAlgebra

		LinearAlgebra.BLAS.set_num_threads(18) #Set number of threads to be used by DiffEqPy if required
		print("BLAS threads were set to:{}".format(Main.eval("ccall((:openblas_get_num_threads64_, Base.libblas_name), Cint, ())"))) #Show number of threads being used by DiffEqPy
	
	toc = time.perf_counter()
	print("Time taken to import 'diffeqpy':{:.2f} s".format(toc - tic))
	
	return diffeqpy_dict
	
def setup_diffeqpy_integrator(diffeqpy_dict,ode_solver_method,ode_func,y0,jac_func=None,t0=0.0,tf = 1.0,dt=1/120.,use_integrator = True):
	"""Setup diffeqpy integrator"""
	
	if ode_solver_method in ['TRBDF2','KenCarp4']:
		ode = diffeqpy_dict["ode"]
		ode_solver = "ode.{}()".format(ode_solver_method) #self.de.TRBDF2()
	elif ode_solver_method in ['CVODE_BDF','ARKODE']:
		Sundials = diffeqpy_dict["Sundials"]
		ode_solver = "Sundials.{}()".format(ode_solver_method)	
		#raise ValueError("Sundials module should be supplied for {}".format(ode_solver_method))
	else:		 
		print("'{}' is not a valid method for diffeqpy ODE solver - switching to default method {}".format(ode_solver_method,ODE_SOLVER_METHOD_DEFAULT))
		ode = diffeqpy_dict["ode"]
		ode_solver = "ode.{}()".format(ODE_SOLVER_METHOD_DEFAULT)
				
	ode_solver = eval(ode_solver)
	if jac_func is not None:
		julia_f = ode.ODEFunction(ode_func, jac=jac_func)
	else:
		julia_f = ode.ODEFunction(ode_func)
	if use_integrator:
		ode_problem = ode.ODEProblem(julia_f, y0, (t0, dt),[])
		integrator = ode.init(ode_problem,ode_solver_method,saveat=dt,abstol=1e-5,reltol=1e-5)#
	else:
		ode_problem = ode.ODEProblem(julia_f, y0, (t0, tf),[])
		integrator = None
	
	return integrator,ode_problem,ode_solver_method

def get_diffeqpy_odeproblem(diffeqpy_dict,ode_func,y0,jac_func=None,t0=0.0,tf = 1.0):
	"""Setup diffeqpy integrator"""	
	
	if jac_func is not None:
		julia_f = diffeqpy_dict["ode"].ODEFunction(ode_func, jac=jac_func)
	else:
		julia_f = diffeqpy_dict["ode"].ODEFunction(ode_func)
	
	ode_problem = diffeqpy_dict["ode"].ODEProblem(julia_f, y0, (t0, tf),[])
		
	return ode_problem

def get_diffeqpy_ssproblem(diffeqpy_dict,ode_problem):
	"""Setup diffeqpy steady state problem"""
		
	ss_problem = diffeqpy_dict["ode"].SteadyStateProblem(ode_problem)
	
	return ss_problem

def get_ode_solver(diffeqpy_dict,ode_problem,ode_solver_method):
	"""Setup diffeqpy integrator"""
	
	if ode_solver_method in ['TRBDF2','KenCarp4']:
		ode = diffeqpy_dict["ode"]
		ode_solver = "ode.{}()".format(ode_solver_method) #self.de.TRBDF2()
	elif ode_solver_method in ['CVODE_BDF','ARKODE']:
		Sundials = diffeqpy_dict["Sundials"]
		ode_solver = "Sundials.{}()".format(ode_solver_method)
		#raise ValueError("Sundials module should be supplied for using {}".format(ode_solver_method))
	else:
		print("'{}' is not a valid method for diffeqpy ODE solver - switching to default method {}".format(ode_solver_method,ODE_SOLVER_METHOD_DEFAULT))
		ode = diffeqpy_dict["ode"]
		ode_solver = "ode.{}()".format(ODE_SOLVER_METHOD_DEFAULT)
	
	ode_solver = eval(ode_solver)
	
	return ode_solver
	
def get_diffeqpy_integrator(diffeqpy_dict,ode_problem,ode_solver,dt = 0.001):
	"""Setup diffeqpy integrator"""
	
	integrator = diffeqpy_dict["ode"].init(ode_problem,ode_solver,saveat=dt,abstol=1e-5,reltol=1e-5)#
	
	return integrator

def solve_diffeqpy_ssproblem(diffeqpy_dict,ss_problem,ss_solver,tspan=1e-9,dt=0.001,use_roots=False):
	"""Setup diffeqpy steady state problem"""
	
	tic = time.perf_counter()
	if not use_roots:
		sol = diffeqpy_dict["ode"].solve(ss_problem,diffeqpy_dict['SteadyStateDiffEq'].DynamicSS(ss_solver),tspan=tspan)
		#sol = diffeqpy_dict['ode'].solve(ss_problem,diffeqpy_dict['SteadyStateDiffEq'].DynamicSS(ss_solver),tspan=tspan,dt=0.001)
	else:
		sol = diffeqpy_dict['ode'].solve(ss_problem,diffeqpy_dict['SteadyStateDiffEq'].SSRootfind())
	
	toc = time.perf_counter()
	print("Time taken to solve steady state problem:{:.2f} s".format(toc - tic))
	
	return sol.u

def step_diffeqpy_integrator(diffeqpy_dict,integrator,dt=0.001):
	"""Integration step using diffeqp"""
	
	diffeqpy_dict["ode"].step_b(integrator,dt,True)
	
	if not diffeqpy_dict["ode"].check_error(integrator) == 'Success':
		raise ValueError("Integration was not successul with return code:{}".format(diffeqpy_dict["ode"].check_error(integrator)))
	
	return integrator.u,np.array([integrator.t])

def solve_diffeqpy_odeproblem(diffeqpy_dict,ode_problem,ode_solver,dt=0.001):
	#Integration step using diffeqp
	
	sol = diffeqpy_dict["ode"].solve(ode_problem,ode_solver,saveat=dt,abstol=1e-5,reltol=1e-5)
	if not sol.retcode == 'Success':
		raise ValueError("Integration was not successul with return code:{}".format(sol.retcode))
		
	return sol.u,sol.t


def create_n_models(modelType='ThreePhaseUnbalanced',configFile= r'../config_der.json',parameterId = '50',
                    standAlone = False,steadyState = False,loop=True,derVerbosity='ERROR',n_models=2):
    """Create n PVDER models"""
    
    PV_DER = []
    sim = []
    results = []
    
    events = SimulationEvents(verbosity = 'DEBUG')
    grid= Grid(events=events,unbalance_ratio_b=1.0,unbalance_ratio_c=1.0)
    Va=164.78-124.57j
    Vb=-190.96-78.26j
    Vc=26.24+206.56j
    Vrms = abs(Va)/math.sqrt(2)
    print('Vrms:{:.2f}'.format(Vrms))
    print('Va:{:.2f},Vb:{:.2f},Vc:{:.2f}'.format(Va,Vb,Vc))
    print('V0:{:.2f}'.format(Va+Vb+Vc))
    
    for i in range(n_models):
        if standAlone:
            
            PV_DER.append(DERModel(modelType=modelType,events=events1,configFile=configFile,
                       gridModel=grid,
                       derId=parameterId,
                       standAlone = standAlone,steadyStateInitialization=steadyState))
        else:
            grid = None
            voltage_scaler = np.random.uniform(low=0.9, high=1.1)
            PV_DER.append(DERModel(modelType=modelType,events=events,configFile=configFile,
                       Vrmsrated = Vrms,
                       gridVoltagePhaseA = Va*voltage_scaler,gridVoltagePhaseB = Vb*voltage_scaler,gridVoltagePhaseC = Vc*voltage_scaler,gridFrequency=2*math.pi*60.0,
                       derId=parameterId,
                       standAlone = standAlone,steadyStateInitialization=steadyState,
                       verbosity = derVerbosity))
        PV_DER[i].DER_model.HVRT_ENABLE = False
        sim.append(DynamicSimulation(gridModel=grid,PV_model=PV_DER[i].DER_model,
                                 events = events,verbosity = 'INFO',solverType='odeint',LOOP_MODE=loop)) #'odeint','ode-vode-bdf'
        results.append(SimulationResults(simulation = sim[i],PER_UNIT=True,verbosity = 'INFO'))
        #PV_DER[i].DER_model.show_PV_DER_parameters('controller_gains')
    return PV_DER,sim,results