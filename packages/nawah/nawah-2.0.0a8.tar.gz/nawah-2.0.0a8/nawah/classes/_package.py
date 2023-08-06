'''Provides 'Env', 'Package', 'App' dataclasses'''

from dataclasses import dataclass
from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Optional)

if TYPE_CHECKING:
    from nawah.types import AnalyticsEvents, NawahDoc

    from ._attr import Attr
    from ._client_app import ClientApp
    from ._job import Job
    from ._module import Module
    from ._sys_doc import SysDoc
    from ._user_setting import UserSetting


@dataclass(kw_only=True)
class Env:
    '''Env dataclass serves role of defining runtime environment config.
    It is used as item for 'envs' App Config Attr. It also serves as base
    for 'Package' dataclass'''

    # pylint: disable=too-many-instance-attributes

    vars: Optional[MutableMapping[str, Any]] = None
    client_apps: Optional[MutableMapping[str, 'ClientApp']] = None
    analytics_events: Optional['AnalyticsEvents'] = None
    conn_timeout: Optional[int] = None
    quota_anon_min: Optional[int] = None
    quota_auth_min: Optional[int] = None
    quota_ip_min: Optional[int] = None
    file_upload_limit: Optional[int] = None
    file_upload_timeout: Optional[int] = None
    data_server: Optional[str] = None
    data_name: Optional[str] = None
    data_ssl: Optional[bool] = None
    data_disk_use: Optional[bool] = None
    cache_server: Optional[str] = None
    cache_db: Optional[int] = 0
    cache_username: Optional[str] = None
    cache_password: Optional[str] = None
    cache_expiry: Optional[int] = None
    error_reporting_server: Optional[str] = None
    locales: Optional[MutableSequence[str]] = None
    locale: Optional[str] = None
    admin_doc: Optional['NawahDoc'] = None
    admin_password: Optional[str] = None
    anon_token: Optional[str] = None
    anon_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None
    user_attrs: Optional[MutableMapping[str, 'Attr']] = None
    user_settings: Optional[MutableMapping[str, 'UserSetting']] = None
    user_doc_settings: Optional[MutableSequence[str]] = None
    groups: Optional[MutableSequence[MutableMapping[str, Any]]] = None
    default_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None
    data_indexes: Optional[MutableSequence[MutableMapping[str, Any]]] = None
    docs: Optional[MutableSequence['SysDoc']] = None
    jobs: Optional[MutableMapping[str, 'Job']] = None
    gateways: Optional[MutableMapping[str, Callable]] = None
    types: Optional[MutableMapping[str, Callable]] = None


@dataclass(kw_only=True)
class Package(Env):
    '''Package dataclass serves role of defining Nawah Package and its config.
    It also serves as base for 'App' dataclass'''

    # pylint: disable=too-many-instance-attributes

    api_level: Optional[str] = None
    version: Optional[str] = None
    vars_types: Optional[MutableMapping[str, 'Attr']] = None
    modules: Optional[MutableSequence[Callable[[], 'Module']]] = None


@dataclass(kw_only=True)
class App(Package):
    '''App dataclass serves role as defining Nawah App and its config'''

    # pylint: disable=too-many-instance-attributes

    name: Optional[str] = None
    version: Optional[str] = None
    debug: Optional[bool] = False
    emulate_test: bool = False
    port: Optional[int] = None
    env: Optional[str] = None
    envs: Optional[MutableMapping[str, Env]] = None
    force_admin_check: Optional[bool] = None
    packages: Optional[MutableSequence[Callable[[], 'Package']]] = None
