'''Provides 'base' Nawah Core Module'''

from nawah.classes import Func, Perm
from nawah.utils import register_module

base = register_module(
    'base',
    desc='\'base\' module provides necessary structure to allow modules to access Base '
    'Functions Callables via \'call\' Utility',
    collection=None,
    attrs=None,
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
        ),
        'create': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
        ),
        'update': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
        ),
        'delete': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
        ),
    },
)
