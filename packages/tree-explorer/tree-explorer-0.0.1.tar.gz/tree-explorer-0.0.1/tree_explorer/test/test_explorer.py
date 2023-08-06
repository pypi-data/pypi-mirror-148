import unittest

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from tree_explorer import TreeExplorer, RandomForestExplorer
from tree_explorer.utils.test import BaseTest


class TestExplorer(BaseTest, unittest.TestCase):

    def test_tree_instance(self):
        self.fit_custom_model(DecisionTreeClassifier, (self.X_train, self.y_train))
        self.assertEqual(isinstance(self.exp, TreeExplorer), True)

    def test_tree_instance_with_autoinfer(self):
        self.fit_custom_model(DecisionTreeClassifier, (self.X_train, self.y_train), auto_infer=False, model_type='tree')
        self.assertEqual(isinstance(self.exp, TreeExplorer), True)

    def test_rf_instance(self):
        self.fit_custom_model(RandomForestClassifier, (self.X_train, self.y_train))
        self.assertEqual(isinstance(self.exp, RandomForestExplorer), True)
