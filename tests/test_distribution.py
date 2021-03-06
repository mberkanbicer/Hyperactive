import numpy as np
from tqdm import tqdm
from hyperactive import Hyperactive


def objective_function(optimizer):
    score = (
        -optimizer.suggested_params["x1"] * optimizer.suggested_params["x1"]
    )
    return score


search_space = {
    "x1": np.arange(-100, 101, 1),
}


def test_multiprocessing_0():
    hyper = Hyperactive(distribution="multiprocessing")
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_multiprocessing_1():
    hyper = Hyperactive(
        distribution={
            "multiprocessing": {
                "initializer": tqdm.set_lock,
                "initargs": (tqdm.get_lock(),),
            }
        }
    )
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_joblib_0():
    hyper = Hyperactive(distribution="joblib")
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)
    hyper.run()


def test_joblib_1():
    from joblib import Parallel, delayed

    def joblib_wrapper(process_func, search_processes_paras, **kwargs):
        n_jobs = len(search_processes_paras)

        jobs = [
            delayed(process_func)(**info_dict)
            for info_dict in search_processes_paras
        ]
        results = Parallel(n_jobs=n_jobs, **kwargs)(jobs)

        return results

    hyper = Hyperactive(distribution=joblib_wrapper)
    hyper.add_search(objective_function, search_space, n_iter=15, n_jobs=2)

    hyper.run()
