'''Provides 'serve_app' Utility'''

import asyncio
import logging
import re
from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Optional, Tuple, Union, cast)

from nawah.classes import App, Attr, Default, Var
from nawah.config import Config
from nawah.enums import VarType
from nawah.exceptions import ConfigException

from ._app import _run_app
from ._config import config_app, config_module
from ._val import deep_update, var_value
from ._validate import validate_attr

if TYPE_CHECKING:
    from nawah.classes import (ClientApp, Env, Job, Module, Package, SysDoc,
                               UserSetting)
    from nawah.types import AnalyticsEvents, NawahDoc


logger = logging.getLogger('nawah')


def serve_app(  # pylint: disable=too-many-locals
    name,
    /,
    *,
    version: str,
    anon_token: 'Var',
    admin_password: 'Var',
    debug: Optional[Union[bool, 'Var']] = False,
    port: Optional[int] = None,
    env: Optional[str] = None,
    envs: Optional[MutableMapping[str, 'Env']] = None,
    force_admin_check: Optional[bool] = None,
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
    packages: Optional[MutableSequence[Callable[[], Tuple[str, 'Package']]]] = None,
):
    '''Returns callable that is used as to serve Nawah App'''

    # pylint: disable=import-outside-toplevel

    from nawah.packages.core import core

    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+([ab][0-9]+)?$', version):
        raise ConfigException(
            f'App \'{name}\' defines invalid \'version\' \'{version}\''
        )

    if debug is True:
        logger.setLevel(logging.DEBUG)
        logger.debug('Set logging level to DEBUG (Config.debug==True)')

    if isinstance(debug, Var):
        if debug.type != VarType.ENV:
            raise ConfigException(
                'Only Var objects of type \'ENV\' can be used in Config Attr. Got '
                f'\'{debug.type}\' for debug Config Attr'
            )
        if var_value(debug):
            logger.setLevel(logging.DEBUG)
            logger.debug('Set logging level to DEBUG (os.environ[Config.debug.var])')
            debug = True

    def _():
        return (
            name,
            App(
                version=version,
                debug=debug,
                port=port,
                env=env,
                envs=envs,
                force_admin_check=force_admin_check,
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
                packages=packages,
            ),
        )

    config_loaders: MutableSequence[Callable[[], Tuple[str, 'Package']]] = [
        core,
        *(packages or []),
        _,
    ]

    for config_loader in config_loaders:
        config_name, config = config_loader()

        for attr_name in config.__dataclass_fields__:
            attr_val = getattr(config, attr_name, None)

            if attr_val is None:
                continue

            if attr_name in ['api_level', 'version', 'modules', 'packages']:
                continue

            # For vars_types Config Attr, preserve config name for debugging purposes
            if attr_name == 'vars_types':
                for var in attr_val:
                    Config.vars_types[var] = {
                        'package': config_name,
                        'type': attr_val[var],
                    }

            # Otherwise, update Config accroding to attr_val type
            elif isinstance(attr_val, list):
                for j in attr_val:
                    getattr(Config, attr_name).append(j)
                if attr_name == 'locales':
                    Config.locales = list(set(Config.locales))

            elif isinstance(attr_val, dict):
                if not getattr(Config, attr_name):
                    setattr(Config, attr_name, {})
                deep_update(target=getattr(Config, attr_name), new_values=attr_val)

            else:
                setattr(Config, attr_name, attr_val)

        config_modules = []
        if module_loaders := getattr(config, 'modules', None):
            module_loaders = cast(
                MutableSequence[Callable[[], Tuple[str, 'Module']]], module_loaders
            )
            for module_loader in module_loaders:
                module_name, module = module_loader()

                if module_name in Config.modules:
                    raise ConfigException(
                        f'Module \'{module_name}\' exist in current runtime config'
                    )

                config_module(module_name=module_name, module=module)
                config_modules.append(module_name)
                Config.modules[module_name] = module

        if getattr(config, 'packages', None):
            pass

        if isinstance(config, App):
            Config.sys.name = config_name
            Config.sys.version = version
        else:
            Config.sys.packages[config_name] = {
                'package': config,
                'modules': config_modules,
            }

    # [DOC] Update User, Session modules with populated attrs
    Config.modules['user'].attrs.update(Config.user_attrs)
    if sum(1 for attr in Config.user_settings if attr in Config.user_attrs) != 0:
        raise ConfigException(
            'At least one attr from \'user_settings\' is conflicting with an attr from '
            '\'user_attrs\''
        )
    for attr in Config.user_doc_settings:
        Config.modules['user'].attrs[attr] = Config.user_settings[attr].val_type
        Config.modules['user'].attrs[attr].default = Config.user_settings[attr].default
    Config.modules['user'].defaults['locale'] = Default(value=Config.locale)

    for user_attr_name, user_attr in Config.user_attrs.items():
        Config.modules['user'].unique_attrs.append(user_attr_name)
        Config.modules['user'].attrs[f'{user_attr_name}_hash'] = Attr.STR()
        session_auth_doc_args = cast(
            MutableSequence[MutableMapping[str, 'Attr']],
            Config.modules['session'].funcs['auth'].doc_attrs,
        )
        session_auth_doc_args.extend(
            [
                {
                    'hash': Attr.STR(),
                    user_attr_name: user_attr,
                    'groups': Attr.LIST(list=[Attr.ID()]),
                },
                {'hash': Attr.STR(), user_attr_name: user_attr},
            ]
        )

    # [DOC] Attempt to validate all packages required vars (via vars_types Config Attr) are met
    for var_name, var in Config.vars_types.items():
        if var_name not in Config.vars:
            raise ConfigException(
                f'Package \'{var["package"]}\' requires \'{var_name}\' Var, but not found in App '
                'Config'
            )
        try:
            validate_attr(
                mode='create',
                attr_name=var_name,
                attr_type=var['type'],
                attr_val=Config.vars[var_name],
            )
        except Exception as e:
            raise ConfigException(
                f'Package \'{var["package"]}\' requires \'{var_name}\' Var of type '
                f'\'{var["type"].type}\', but validation failed'
            ) from e

    asyncio.run(config_app())
    _run_app()
