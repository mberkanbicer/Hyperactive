from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

from hyperactive import Hyperactive

data = load_iris()
X, y = data.data, data.target


def model(para, X, y):
    knr = KNeighborsClassifier(n_neighbors=para["n_neighbors"])
    scores = cross_val_score(knr, X, y, cv=5)
    score = scores.mean()

    return score


search_space = {
    "n_neighbors": list(range(1, 100)),
}

optimizer = "RandomRestartHillClimbing"

hyper = Hyperactive(X, y)
hyper.add_search(model, search_space, optimizer=optimizer, n_iter=100)
hyper.run()


optimizer = {
    "RandomRestartHillClimbing": {
        "epsilon": 0.1,
        "distribution": "laplace",
        "n_neighbours": 4,
        "n_restarts": 20,
    },
}

hyper = Hyperactive(X, y)
hyper.add_search(model, search_space, optimizer=optimizer, n_iter=100)
hyper.run()
