from tree_explorer.explorers import TreeExplorer, RandomForestExplorer
from tree_explorer.utils.validation import get_model_type, validate_model_type


class Explorer(object):

    """

    """

    @staticmethod
    def _return_explorer_instance(model,
                                  model_type: str):
        if model_type == 'tree':
            return TreeExplorer(tree_model=model)
        elif model_type == 'random_forest':
            return RandomForestExplorer(rf_model=model)

    def __new__(cls,
                model,
                auto_infer: bool = True,
                model_type=None):
        if auto_infer:
            return Explorer._return_explorer_instance(model, get_model_type(model))
        else:
            if validate_model_type(model_type):
                return Explorer._return_explorer_instance(model, model_type)
