from sklearn.model_selection import cross_val_score
from lightgbm import LGBMRegressor
from sklearn.datasets import load_diabetes
from hyperactive import Hyperactive

data = load_diabetes()
X, y = data.data, data.target


def model(para, X, y):
    lgbm = LGBMRegressor(
        num_leaves=para["num_leaves"],
        bagging_freq=para["bagging_freq"],
        learning_rate=para["learning_rate"],
    )
    scores = cross_val_score(lgbm, X, y, cv=3)

    return scores.mean()


search_space = {
    "num_leaves": list(range(2, 50)),
    "bagging_freq": list(range(2, 12)),
    "learning_rate": [1e-3, 1e-2, 1e-1, 0.5, 1.0],
}


hyper = Hyperactive(X, y)
hyper.add_search(model, search_space, n_iter=30)
hyper.run()
