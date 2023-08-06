import numpy as np
import pandas as pd


# TODO: aggiungere coefficiente che calcoli over fitting struttura

class BaseTreeExplorer:

    def __init__(self,
                 children_left: np.ndarray,
                 children_right: np.ndarray,
                 node_count: np.ndarray,
                 n_node_samples: np.ndarray,
                 impurity: np.ndarray,
                 feature: np.ndarray,
                 threshold: np.ndarray):
        self.children_left = children_left
        self.children_right = children_right
        self.node_count = node_count
        self.n_node_samples = n_node_samples
        self.impurity = impurity
        self.feature = feature
        self.threshold = threshold

    # TODO: aggiungere overfitting sulle features e interazione features

    @staticmethod
    def build_unique_dict(array: np.ndarray,
                          pct: bool):
        unique, counts = np.unique(array, return_counts=True)
        if pct:
            counts = counts / counts.sum()
        return dict(zip(unique, counts))

    def _get_node_depth(self):
        node_depth = np.zeros(shape=self.node_count, dtype=np.int64)
        stack = [(0, 0)]
        while len(stack) > 0:
            node_id, depth = stack.pop()
            node_depth[node_id] = depth
            is_split_node = self.children_left[node_id] != self.children_right[node_id]
            if is_split_node:
                stack.append((self.children_left[node_id], depth + 1))
                stack.append((self.children_right[node_id], depth + 1))
        return node_depth

    def _get_leaves(self):
        return self.children_right == -1

    def _get_samples_dist(self):
        return self.n_node_samples[self._get_leaves()]

    def get_leaves_depth(self):
        return self._get_node_depth()[self._get_leaves()]

    def _get_leaves_per_depth(self, pct):
        leaves_per_depth = BaseTreeExplorer.build_unique_dict(self.get_leaves_depth(), pct)
        return pd.Series(leaves_per_depth, name='leaves').to_frame()

    def get_impurity_dist(self):
        return self.impurity[self._get_leaves() == False]

    def get_feature_split(self,
                          names: list,
                          feature):
        index = names.index(feature)
        return sorted(self.threshold[self.feature == index])

    def _get_samples_per_depth(self,
                               pct: bool):
        samples_dist = self._get_samples_dist()
        samples_depth = self.get_leaves_depth()
        samples_frame = pd.DataFrame(data=np.c_[samples_dist,
                                                samples_depth],
                                     columns=['samples_dist', 'sample_depth'])
        if not pct:
            return samples_frame.groupby('sample_depth').samples_dist.sum().to_frame()
        else:
            samples_per_depth = samples_frame.groupby('sample_depth').samples_dist.sum().to_frame()
            return samples_per_depth / samples_per_depth.values.sum()
