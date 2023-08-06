from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split

from tree_explorer import Explorer


class BaseTest:

    def fit_custom_model(self,
                         model,
                         train_set: tuple,
                         auto_infer=True,
                         model_type=None,
                         *args, **kwargs) -> None:
        clf = model(*args, **kwargs)
        self.clf = clf.fit(train_set[0], train_set[1])
        self.exp = Explorer(model=self.clf, auto_infer=auto_infer, model_type=model_type)

    def setUp(self) -> None:
        X, y = make_blobs(n_samples=1000, centers=2, n_features=10,
                          random_state=0, cluster_std=4)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3)

    def tearDown(self) -> None:
        attrs = ['exp', 'clf', 'X_train', 'X_test', 'y_train', 'y_text']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
