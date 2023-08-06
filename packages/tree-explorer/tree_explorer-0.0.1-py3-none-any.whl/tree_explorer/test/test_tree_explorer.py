import unittest

import numpy as np
from sklearn.tree import DecisionTreeClassifier

from tree_explorer.utils.test import BaseTest


class TestTreeExplorer(BaseTest, unittest.TestCase):

    def test_max_depth(self):
        self.fit_custom_model(model=DecisionTreeClassifier,
                              train_set=(self.X_train, self.y_train), max_depth=5)
        self.assertLessEqual(np.max(self.exp.get_leaves_depth()), 5)

    def test_leaf_simmetry(self):
        self.fit_custom_model(model=DecisionTreeClassifier,
                              train_set=(self.X_train, self.y_train))
        self.assertEqual(all((self.exp.children_left == -1) == (self.exp.children_right == -1)), True)

    def test_leaf_count(self):
        self.fit_custom_model(model=DecisionTreeClassifier,
                              train_set=(self.X_train, self.y_train), max_leaf_nodes=3)
        self.assertLessEqual(self.exp._get_leaves().sum(), 3)

    def test_none_call(self):
        # test call without additional arguments
        self.fit_custom_model(model=DecisionTreeClassifier,
                              train_set=(self.X_train, self.y_train), max_leaf_nodes=5)
        self.assertEqual(self.exp.get_samples_dist(None).sum(), self.X_train.shape[0])
        self.assertEqual(self.exp.get_samples_dist(data=None).sum(), self.X_train.shape[0])
        self.assertEqual(self.exp.get_samples_dist(data=self.X_test).sum(), self.X_test.shape[0])
        self.assertEqual(self.exp.get_samples_dist(self.X_test).sum(), self.X_test.shape[0])
        # test call with additional arguments
        # calls with default args
        self.assertEqual(self.exp.get_samples_per_depth().values.sum(), self.X_train.shape[0])
        self.assertEqual(self.exp.get_samples_per_depth(data=None).values.sum(), self.X_train.shape[0])
        self.assertEqual(self.exp.get_samples_per_depth(None).values.sum(), self.X_train.shape[0])
        # calls specifying additional args value
        self.assertEqual(self.exp.get_samples_per_depth(pct=True).values.sum(), 1)
        self.assertEqual(self.exp.get_samples_per_depth(data=None, pct=True).values.sum(), 1)
        self.assertEqual(self.exp.get_samples_per_depth(None, pct=True).values.sum(), 1)
        # calls with test set
        self.assertEqual(self.exp.get_samples_per_depth(data=self.X_test, pct=True).values.sum(), 1)
        self.assertEqual(self.exp.get_samples_per_depth(data=self.X_test, pct=False).values.sum(), self.X_test.shape[0])
        self.assertEqual(self.exp.get_samples_per_depth(data=self.X_test).values.sum(), self.X_test.shape[0])

    def test_input_validation(self):
        self.fit_custom_model(model=DecisionTreeClassifier,
                              train_set=(self.X_train, self.y_train))
        self.assertRaises(ValueError,
                          self.exp.get_metric_per_depth, data=self.X_test,
                          y_pred=self.clf.predict(self.X_test),
                          y_true=self.y_test,
                          metric='not a callable')
