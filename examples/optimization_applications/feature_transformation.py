import numpy as np
import itertools
from sklearn.datasets import load_boston
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from hyperactive import Hyperactive

data = load_boston()
X, y = data.data, data.target


def model(para, X, y):
    feature_list = []
    for key in para.keys():
        if "feature" not in key:
            continue

        nth_feature = int(key.rsplit(".", 1)[1])

        if para[key] is False:
            continue
        elif para[key] is True:
            feature = X[:, nth_feature]
            feature_list.append(feature)
        else:
            feature = para[key](X[:, nth_feature])
            feature_list.append(feature)

    X_new = np.array(feature_list).T

    knr = KNeighborsRegressor(n_neighbors=para["n_neighbors"])
    scores = cross_val_score(knr, X_new, y, cv=5)
    score = scores.mean()

    return score


features_search_space = [True, False, np.log, np.square, np.sqrt, np.sin, np.cos]

search_space = {
    "n_neighbors": list(range(1, 100)),
    "feature.0": features_search_space,
    "feature.1": features_search_space,
    "feature.2": features_search_space,
    "feature.3": features_search_space,
    "feature.4": features_search_space,
    "feature.5": features_search_space,
    "feature.6": features_search_space,
    "feature.7": features_search_space,
    "feature.8": features_search_space,
    "feature.9": features_search_space,
    "feature.10": features_search_space,
    "feature.11": features_search_space,
    "feature.12": features_search_space,
}


hyper = Hyperactive(X, y)
hyper.add_search(model, search_space, n_iter=1500)
hyper.run()
