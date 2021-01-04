from copy import deepcopy
from functools import reduce
from typing import Any

import environ


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Merges dicts.
    modified from https://gist.github.com/yatsu/68660bea18edfe7e023656c250661086
    """
    for key in dict2:
        if key not in dict1 or not isinstance(dict1[key], dict):
            dict1[key] = deepcopy(dict2[key])
        else:
            dict1[key] = merge_dicts(dict1[key], dict2[key])
    return dict1


def deep_merge_dicts(*dicts: dict, update: bool = False) -> dict:
    """
    Merges dicts deeply.
    modified from https://gist.github.com/yatsu/68660bea18edfe7e023656c250661086
    """
    if update:
        return reduce(merge_dicts, dicts[1:], dicts[0])
    return reduce(merge_dicts, dicts, {})


class Env(environ.Env):
    def __init__(self, path: str = None, **scheme):
        super().__init__(**scheme)
        if path:
            self.read_env(path)

    def cache_opts(
            self,
            var: str = 'CACHE_URL',
            default: Any = environ.Env.NOTSET,
            backend: str = None,
            options: dict = None) -> dict:
        cache_config = self.cache(var, default=default, backend=backend)
        return deep_merge_dicts(cache_config, options or {})

    def db_opts(
            self,
            var: str = 'DATABASE_URL',
            default: Any = environ.Env.NOTSET,
            engine: str = None,
            options: dict = None) -> dict:
        db_config = self.db(var, default=default, engine=engine)
        return deep_merge_dicts(db_config, options or {})
