import pytest
import numpy as np


from hyperactive import Hyperactive
from hyperactive.optimizers.strategies import CustomOptimizationStrategy

from ._parametrize import optimizers, optimizers_strat


def objective_function(opt):
    score = -(opt["x1"] * opt["x1"] + opt["x2"] * opt["x2"])
    return score


search_space = {
    "x1": list(np.arange(-12, 15, 1)),
    "x2": list(np.arange(-8, 20, 1)),
}


@pytest.mark.parametrize(*optimizers)
@pytest.mark.parametrize(*optimizers_strat)
def test_strategy_multiprocessing_0(Optimizer, Optimizer_strat):
    optimizer1 = Optimizer()
    optimizer2 = Optimizer_strat()

    opt_strat = CustomOptimizationStrategy()
    opt_strat.add_optimizer(optimizer1, duration=0.5)
    opt_strat.add_optimizer(optimizer2, duration=0.5)

    n_iter = 30

    hyper = Hyperactive()
    hyper.add_search(
        objective_function,
        search_space,
        optimizer=opt_strat,
        n_iter=n_iter,
        n_jobs=2,
    )
    hyper.run()


@pytest.mark.parametrize(*optimizers)
@pytest.mark.parametrize(*optimizers_strat)
def test_strategy_multiprocessing_1(Optimizer, Optimizer_strat):
    optimizer1 = Optimizer()
    optimizer2 = Optimizer_strat()

    opt_strat = CustomOptimizationStrategy()
    opt_strat.add_optimizer(optimizer1, duration=0.5)
    opt_strat.add_optimizer(optimizer2, duration=0.5)

    n_iter = 30

    hyper = Hyperactive()
    hyper.add_search(
        objective_function,
        search_space,
        optimizer=opt_strat,
        n_iter=n_iter,
        n_jobs=1,
    )
    hyper.add_search(
        objective_function,
        search_space,
        optimizer=opt_strat,
        n_iter=n_iter,
        n_jobs=1,
    )
    hyper.add_search(
        objective_function,
        search_space,
        optimizer=opt_strat,
        n_iter=n_iter,
        n_jobs=1,
    )
    hyper.run()