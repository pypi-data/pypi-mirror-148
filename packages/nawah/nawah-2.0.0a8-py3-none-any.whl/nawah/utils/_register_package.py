'''Provides 'register_package' Utility'''

import re
from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Optional, Tuple, Union)

from nawah.classes import Package

if TYPE_CHECKING:
    from nawah.classes import (Attr, ClientApp, Job, Module, SysDoc,
                               UserSetting, Var)
    from nawah.types import AnalyticsEvents, NawahDoc


def register_package(  # pylint: disable=too-many-locals
    name,
    /,
    *,
    api_level: str,
    version: str,
    vars_types: Optional[MutableMapping[str, 'Attr']] = None,
    vars: Optional[  # pylint: disable=redefined-builtin
        MutableMapping[str, Any]
    ] = None,
    client_apps: Optional[MutableMapping[str, 'ClientApp']] = None,
    analytics_events: Optional['AnalyticsEvents'] = None,
    conn_timeout: Optional[Union[int, 'Var']] = None,
    quota_anon_min: Optional[Union[int, 'Var']] = None,
    quota_auth_min: Optional[Union[int, 'Var']] = None,
    quota_ip_min: Optional[Union[int, 'Var']] = None,
    file_upload_limit: Optional[Union[int, 'Var']] = None,
    file_upload_timeout: Optional[Union[int, 'Var']] = None,
    data_server: Optional[Union[str, 'Var']] = None,
    data_name: Optional[Union[str, 'Var']] = None,
    data_ssl: Optional[Union[bool, 'Var']] = None,
    data_disk_use: Optional[Union[bool, 'Var']] = None,
    cache_server: Optional[Union[str, 'Var']] = None,
    cache_db: Optional[Union[int, 'Var']] = 0,
    cache_username: Optional[Union[str, 'Var']] = None,
    cache_password: Optional[Union[str, 'Var']] = None,
    cache_expiry: Optional[Union[int, 'Var']] = None,
    error_reporting_server: Optional[Union[str, 'Var']] = None,
    locales: Optional[MutableSequence[str]] = None,
    locale: Optional[str] = None,
    admin_doc: Optional['NawahDoc'] = None,
    admin_password: Optional[str] = None,
    anon_token: Optional[str] = None,
    anon_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None,
    user_attrs: Optional[MutableMapping[str, 'Attr']] = None,
    user_settings: Optional[MutableMapping[str, 'UserSetting']] = None,
    user_doc_settings: Optional[MutableSequence[str]] = None,
    groups: Optional[MutableSequence[MutableMapping[str, Any]]] = None,
    default_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None,
    data_indexes: Optional[MutableSequence[MutableMapping[str, Any]]] = None,
    docs: Optional[MutableSequence['SysDoc']] = None,
    jobs: Optional[MutableMapping[str, 'Job']] = None,
    gateways: Optional[MutableMapping[str, Callable]] = None,
    types: Optional[MutableMapping[str, Callable]] = None,
    modules: Optional[MutableSequence[Callable[[], Tuple[str, 'Module']]]] = None,
) -> Callable[[], Tuple[str, 'Package']]:
    '''Returns callable that is used as item for 'packages' App Config Attr'''

    if not re.match(r'^[0-9]+\.[0-9]+$', api_level):
        raise Exception(
            f'Package \'{name}\' defines invalid \'api_level\' \'{api_level}\''
        )

    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+([ab][0-9]+)?$', version):
        raise Exception(f'Package \'{name}\' defines invalid \'version\' \'{version}\'')

    def _():
        return (
            name,
            Package(
                api_level=api_level,
                version=version,
                vars_types=vars_types,
                vars=vars,
                client_apps=client_apps,
                analytics_events=analytics_events,
                conn_timeout=conn_timeout,
                quota_anon_min=quota_anon_min,
                quota_auth_min=quota_auth_min,
                quota_ip_min=quota_ip_min,
                file_upload_limit=file_upload_limit,
                file_upload_timeout=file_upload_timeout,
                data_server=data_server,
                data_name=data_name,
                data_ssl=data_ssl,
                data_disk_use=data_disk_use,
                cache_server=cache_server,
                cache_username=cache_username,
                cache_password=cache_password,
                cache_db=cache_db,
                cache_expiry=cache_expiry,
                error_reporting_server=error_reporting_server,
                locales=locales,
                locale=locale,
                admin_doc=admin_doc,
                admin_password=admin_password,
                anon_token=anon_token,
                anon_privileges=anon_privileges,
                user_attrs=user_attrs,
                user_settings=user_settings,
                user_doc_settings=user_doc_settings,
                groups=groups,
                default_privileges=default_privileges,
                data_indexes=data_indexes,
                docs=docs,
                jobs=jobs,
                gateways=gateways,
                types=types,
                modules=modules,
            ),
        )

    return _
