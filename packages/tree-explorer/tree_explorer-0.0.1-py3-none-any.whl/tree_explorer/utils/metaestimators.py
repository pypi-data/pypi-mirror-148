import inspect
from tree_explorer.utils import partial_update, get_default_args


def merge_default_arguments(f, args, kwargs):
    all_args = list(inspect.signature(f).parameters.keys())
    _ = all_args.remove('self')
    all_args_dict = {}
    if len(args) > 0:
        for i, arg in enumerate(args):
            all_args_dict[all_args[i]] = arg
    all_args_dict = partial_update(all_args_dict, kwargs)
    all_args_dict = partial_update(all_args_dict, get_default_args(f))
    return all_args_dict


def call_if_none(method, argument):
    def decorator(f):
        def wrapped(self, *args, **kwargs):
            all_args = merge_default_arguments(f, args, kwargs)
            if isinstance(all_args[argument], type(None)):
                return getattr(self, method)(**{k: v for k, v in all_args.items() if k not in [argument, 'self']})
            else:
                return f(self, *args, **kwargs)

        return wrapped

    return decorator
