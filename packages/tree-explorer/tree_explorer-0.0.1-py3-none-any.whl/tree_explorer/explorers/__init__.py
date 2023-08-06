import numpy as np
import pandas as pd

from tree_explorer.utils.validation import check_input, validate_datatypes
from tree_explorer.utils.metaestimators import call_if_none
from tree_explorer.base import BaseTreeExplorer


class TreeExplorer(BaseTreeExplorer):

    @check_input
    def __init__(self, tree_model):
        super().__init__(children_left=tree_model.tree_.children_left,
                         children_right=tree_model.tree_.children_right,
                         node_count=tree_model.tree_.node_count,
                         n_node_samples=tree_model.tree_.n_node_samples,
                         impurity=tree_model.tree_.impurity,
                         feature=tree_model.tree_.feature,
                         threshold=tree_model.tree_.threshold)
        self.tree = tree_model

    @validate_datatypes
    @call_if_none(method='_get_samples_dist', argument='data')
    def get_samples_dist(self, data=None):
        leaf_idx = self.tree.apply(data)
        _, sample_dist = np.unique(leaf_idx, return_counts=True)
        return sample_dist

    @validate_datatypes
    @call_if_none(method='_get_leaves_per_depth', argument='data')
    def get_leaves_per_depth(self, data=None, pct=False):
        leaf_depths = self._get_node_depth()[self.tree.apply(data)]
        leaves_per_depth = BaseTreeExplorer.build_unique_dict(leaf_depths, pct)
        return pd.Series(leaves_per_depth, name='leaves').to_frame()

    @validate_datatypes
    @call_if_none(method='_get_samples_per_depth', argument='data')
    def get_samples_per_depth(self, data=None, pct=False):
        leaf_id = self.tree.apply(data)
        leaf_depths = self._get_node_depth()[self.tree.apply(data)]
        samples_frame = pd.DataFrame(data=np.c_[leaf_id,
                                                leaf_depths],
                                     columns=['leaf_id', 'leaf_depths'])
        if not pct:
            return samples_frame.groupby('leaf_depths').leaf_id.count().to_frame()
        else:
            samples_per_depth = samples_frame.groupby('leaf_depths').leaf_id.count().to_frame().rename(
                columns={'leaf_id': 'n_samples'})
            return samples_per_depth / samples_per_depth.values.sum()

    @check_input
    @validate_datatypes
    def get_metric_per_depth(self,
                             data,
                             y_pred,
                             y_test,
                             metric, **kwargs):
        sample_depths = self.tree.tree_.decision_path(data).toarray().sum(axis=1) - 1
        metric_frame = pd.DataFrame(data=np.c_[sample_depths,
                                               y_pred,
                                               y_test],
                                    columns=['sample_depths', 'y_pred', 'y_true'])

        return metric_frame.groupby('sample_depths').apply(
            lambda x: metric(x.y_pred, x.y_true, **kwargs)).to_frame().rename(columns={0: metric.__name__})


class BaseEnsembleExplorer:

    def __init__(self, estimators):
        self.estimators = estimators
        self.explorers = [TreeExplorer(estimator) for estimator in estimators]

    def get_full_leaves_depths(self):
        return np.hstack([explorer.get_leaves_depth() for explorer in self.explorers])

    def get_full_samples(self):
        return np.hstack([explorer.get_samples_dist() for explorer in self.explorers])

    def get_n_leaves(self):
        return np.array([len(explorer._get_leaves()) for explorer in self.explorers])


class RandomForestExplorer(BaseEnsembleExplorer):

    @check_input
    def __init__(self, rf_model):
        super().__init__(rf_model.estimators_)

    @check_input
    def get_metric_over_n_estimators(self,
                                     data,
                                     y_true,
                                     is_proba,
                                     metric):
        # TODO: mi sembra sbagliata la logica is proba
        n_estimators = [i for i in range(1, len(self.estimators) + 1)]
        preds = np.zeros(shape=(len(self.estimators), data.shape[0]))
        for i, tree in enumerate(self.estimators):
            preds[i, :] = tree.predict_proba(data)[:, 1]
        if not is_proba:
            preds = np.round(np.cumsum(preds, axis=0) / np.array(n_estimators).reshape(-1, 1))
        return n_estimators, [metric(y_true, pred) for pred in preds]

    @check_input
    def get_metric_over_estimators(self,
                                   data,
                                   y_true,
                                   is_proba,
                                   metric, **kwargs):
        if is_proba:
            return [metric(y_true, tree.predict_proba(data)) for tree in self.estimators]
        else:
            return [metric(y_true, tree.predict(data), **kwargs) for tree in self.estimators]

    def get_metric_per_depth(self,
                             data,
                             y_pred,
                             y_test,
                             metric,
                             **kwargs):
        return [explorer.get_metric_per_depth(data,
                                              y_pred,
                                              y_test,
                                              metric, **kwargs) for explorer in self.explorers]

    def get_samples_per_depth(self, data=None, pct=False):
        return [explorer.get_samples_per_depth(data, pct) for explorer in self.explorers]

    def get_samples_dist(self, data=None):
        return [explorer.get_samples_dist(data) for explorer in self.explorers]

    def get_top_tree(self,
                     k,
                     data,
                     y_true,
                     is_proba,
                     metric, **kwargs):
        metric_values = sorted(self.get_metric_over_estimators(data,
                                                               y_true,
                                                               is_proba,
                                                               metric, **kwargs))

        return [self.estimators[metric_values.index(v)] for v in metric_values[:k]]
