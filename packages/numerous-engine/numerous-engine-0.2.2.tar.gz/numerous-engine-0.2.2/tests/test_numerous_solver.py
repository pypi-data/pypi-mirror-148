from numerous.engine.system import Subsystem, Item
from numerous.multiphysics import EquationBase, Equation
from numerous.engine.model import Model
from numerous.engine.simulation import Simulation
from numerous.engine.simulation.solvers.base_solver import SolverType
from numerous.utils.logger_levels import LoggerLevel
from numerous.utils.historian import InMemoryHistorian
import pytest
from pytest import approx

class AbsTestSystem(Subsystem):
    def __init__(self, tag='abstestsys', item: Item=None):
        super(AbsTestSystem, self).__init__(tag)
        self.register_item(item)


class AbsTestItem(Item, EquationBase):
    def __init__(self, tag='abstest'):
        super(AbsTestItem, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_state('x', 0, logger_level=LoggerLevel.INFO)
        self.add_state('y', 10, logger_level=LoggerLevel.INFO)
        self.add_constant('x_max', 1)
        self.add_constant('k', 0.01)
        self.t1.add_equations([self])

    @Equation()
    def eval(self, scope):

        x_dot = 0
        y_dot = 0.001*(scope.x-scope.y)

        if scope.y < 0:
            if scope.x <= scope.x_max:
                x_dot = - scope.k * scope.y
        if scope.y > 0:
            if scope.x >= -scope.x_max:
                x_dot = - scope.k * scope.y


        scope.x_dot = x_dot
        scope.y_dot = y_dot

@pytest.fixture
def model():
    sys = AbsTestSystem(item=AbsTestItem())
    historian=InMemoryHistorian()
    historian.max_size = 2000
    model = Model(system=sys, logger_level=LoggerLevel.INFO, use_llvm=True, historian=historian)
    yield model

@pytest.fixture
def variables(model: Model):
    variables = model.get_variables()
    yield variables

@pytest.fixture
def simulation(model: Model, variables: variables):
    def fn(solver: SolverType, method: str):

        model.update_variables(variables)
        sim = Simulation(model, t_start=0, t_stop=1000, num=1000, solver_type=solver, method=method)
        sim.reset()
        sim.model.historian_df = None
        return sim
    yield fn

@pytest.fixture
def step_solver(simulation: simulation):
    def fn(solver: SolverType, method: str):
        sim = simulation(solver=solver, method=method)
        t = 0
        dt = 1
        while True:
            sim.step_solve(t, dt)
            t += dt
            if t >= 1000:
                break
        sim.model.create_historian_df()
        df = sim.model.historian_df
        return df
    yield fn

@pytest.fixture()
def normal_solver(simulation: simulation):
    def fn(solver: SolverType, method: str):
        sim = simulation(solver=solver, method=method)
        sim.solve()
        df = sim.model.historian_df
        return df
    yield fn

def test_numerous_solver(normal_solver: normal_solver, step_solver: step_solver):
    rel = 1e-6
    df_step = step_solver(solver=SolverType.NUMEROUS, method='RK45')
    df_normal_solver = normal_solver(solver=SolverType.NUMEROUS, method='RK45')

    assert df_step['abstestsys.abstest.t1.x'].values == approx(df_normal_solver['abstestsys.abstest.t1.x'].values, rel=rel), \
        f"results do not match within relative tolerance {rel}"