'''Provides 'core' Nawah Package'''

from nawah.utils import register_package

from .base import base
from .file import file
from .group import group
from .session import session
from .setting import setting
from .user import user

core = register_package(
    'core',
    api_level='2.0',
    version='2.0.0',
    modules=[base, user, group, session, setting, file],
)
