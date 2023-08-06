import inspect


def partial_update(dict_to_update, dict_):
    for key, value in dict_.items():
        if key not in dict_to_update.keys():
            dict_to_update[key] = value
    return dict_to_update


def get_default_args(func, exclude=None):
    signature = inspect.signature(func)
    kwargs = {k: v.default
              for k, v in signature.parameters.items()
              if v.default is not inspect.Parameter.empty}
    if isinstance(exclude, list):
        return {k: v for k, v in kwargs.items() if k not in exclude}
    else:
        return kwargs
