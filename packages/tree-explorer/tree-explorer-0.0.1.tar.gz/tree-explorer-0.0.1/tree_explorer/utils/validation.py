import numpy as np
import pandas as pd


def check_input(f):
    def wrapped(*args, **kwargs):
        for key, value in kwargs.items():

            if 'tree' in key:
                if not hasattr(value, 'tree_'):
                    raise AttributeError('Model provided does not have a tree_ attribute')
            elif 'rf_model' in key:
                if not hasattr(value, 'estimators_'):
                    raise AttributeError('Model provided does not have an estimators_ attribute')
            elif 'metric' in key:
                if not callable(value):
                    raise ValueError('Metric provided is not a callable')

        return f(*args, **kwargs)

    return wrapped


def validate_datatypes(f):
    def wrapped(*args, **kwargs):

        casted_args = []
        for i, value in enumerate(args):
            if isinstance(args[i], np.ndarray):
                casted_args.append(args[i].astype(np.float32))
            elif isinstance(args[i], pd.core.frame.DataFrame):
                casted_args.append(args[i].values.astype(np.float32))
            else:
                casted_args.append(args[i])

        return f(*tuple(casted_args), **kwargs)

    return wrapped


def get_model_type(model):
    if 'tree' in str(model).lower():
        return 'tree'
    elif 'randomforest' in str(model).lower():
        return 'random_forest'
    else:
        raise ValueError('failed to infer the model_type. Please provide it through the model_type argument')


def validate_model_type(model_type):
    if isinstance(model_type, type(None)):
        raise ValueError('If autoinfer is set to False a model type must be provided')
    elif not isinstance(model_type, str):
        raise ValueError('model_type arugment should be  a string')
    else:
        if model_type not in ['tree', 'random_forest']:
            raise ValueError('model_type should tree or random_forest')

    return True
