import unittest

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from tree_explorer.utils.test import BaseTest


class TestRFExplorer(BaseTest, unittest.TestCase):

    def test_arrays_shape(self):
        self.fit_custom_model(model=RandomForestClassifier,
                              train_set=(self.X_train, self.y_train),
                              n_estimators=10)
        estimators, metric = self.exp.get_metric_over_n_estimators(data=self.X_test,
                                                                   y_true=self.y_test,
                                                                   is_proba=False,
                                                                   metric=accuracy_score
                                                                   )
        # check shapes of generated array
        self.assertEqual(10, len(metric))
        self.assertEqual(10, len(estimators))

    def test_metric_over_n_estimators(self):
        self.fit_custom_model(model=RandomForestClassifier,
                              train_set=(self.X_train, self.y_train),
                              n_estimators=20)
        estimators, metric = self.exp.get_metric_over_n_estimators(data=self.X_test,
                                                                   y_true=self.y_test,
                                                                   is_proba=False,
                                                                   metric=accuracy_score
                                                                   )
        score = accuracy_score(self.y_test, self.clf.predict(self.X_test))
        self.assertEqual(metric[-1], score)
