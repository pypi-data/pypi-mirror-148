'''Provides 'call' Utility'''

import asyncio
import datetime
import inspect
import logging
import re
from typing import (TYPE_CHECKING, Any, Awaitable, Callable, MutableMapping,
                    MutableSequence, Union, cast)

from nawah.classes import Query, Var
from nawah.config import Config
from nawah.enums import Event, VarType
from nawah.exceptions import (FuncException, InvalidAttrException,
                              InvalidCallEndpointException,
                              InvalidDocAttrException, InvalidFuncException,
                              InvalidModuleException,
                              InvalidQueryAttrException,
                              MissingDocAttrException,
                              MissingQueryAttrException)

from ._cache import _get_cache, _set_cache
from ._check_permissions import check_permissions as check_permissions_utility
from ._val import camel_to_upper, var_value
from ._validate import validate_attr

if TYPE_CHECKING:
    from nawah.classes import Attr
    from nawah.types import (NawahDoc, NawahEnv, NawahEvents, NawahQuery,
                             Results)


logger = logging.getLogger('nawah')


async def call(
    endpoint: str,
    /,
    *,
    module_name: str = None,
    skip_events: 'NawahEvents' = None,
    env: 'NawahEnv' = None,
    query: 'NawahQuery' = None,
    doc: 'NawahDoc' = None,
    args: MutableMapping[str, Any] = None,
) -> Awaitable['Results']:
    '''Checks validity of an endpoint and calls Nawah Function callable at endpoint,
    returning the couroutine of the callable. If endpoint points to non-existent
    Nawah Function, raises 'InvalidFuncException'.'''

    if not re.match(r'^[a-z_]+\/[a-z_]+$', endpoint):
        raise InvalidCallEndpointException(endpoint=endpoint)

    endpoint_module, endpoint_func = endpoint.split('/')

    try:
        module = Config.modules[endpoint_module]
    except KeyError as e:
        raise InvalidModuleException(module_name=endpoint_module) from e

    try:
        func = module.funcs[endpoint_func]
    except KeyError as e:
        raise InvalidFuncException(
            module_name=endpoint_module, func_name=endpoint_func
        ) from e

    # Set defaults for kwargs
    module_name = module_name or endpoint_module
    skip_events = skip_events or []
    query = query or []
    doc = doc or {}
    env = env or {}

    # Convert query to Query object
    query = Query(query)

    # Check conditions for call checks
    check_permissions = (
        check_attrs_query
    ) = check_attrs_doc = check_cache = check_analytics = True

    check_permissions = Event.PERM not in skip_events
    check_cache = Event.CACHE not in skip_events
    check_attrs_query = check_attrs_doc = Event.ATTRS not in skip_events
    check_analytics = Event.ANALYTICS not in skip_events
    if check_attrs_query:
        check_attrs_query = Event.ATTRS_QUERY not in skip_events
    if check_attrs_doc:
        check_attrs_doc = Event.ATTRS_DOC not in skip_events

    if check_permissions:
        query_mod, doc_mod = check_permissions_utility(func=func, env=env)
        # Use return of check_permissions_utility to update query, doc
        _process_query_mod(
            query=query,
            query_mod=query_mod,
            env=env,
            doc=doc,
        )
        _process_doc_mod(
            doc=doc,
            doc_mod=doc_mod,
            env=env,
            query=query,
        )

    if check_attrs_query:
        func.query_attrs = cast(MutableSequence, func.query_attrs)
        _check_query_attrs(query=query, query_attrs=func.query_attrs)

    if check_attrs_doc:
        func.doc_attrs = cast(MutableSequence, func.doc_attrs)
        _check_doc_attrs(doc=doc, doc_attrs=func.doc_attrs)

    if check_cache:
        cache_key, call_cache = await _get_cache(
            func=func,
            skip_events=skip_events,
            env=env,
            query=query,
        )

        if call_cache:
            return call_cache

    if check_analytics:
        # [TODO] Implement
        pass

    try:
        func_callable = cast(Callable, func.callable)
        kwargs: MutableMapping = {
            'func': func,
            'module_name': module_name,
            'skip_events': skip_events,
            'env': env,
            'query': query,
            'doc': doc,
            'args': args,
        }
        results = await func_callable(
            **{
                param: kwargs[param]
                for param in inspect.signature(func_callable).parameters
                if param in kwargs
            }
        )
    except Exception as e:
        raise FuncException(
            status=getattr(e, 'status', 500),
            msg=e.args[0] if e.args else 'Unexpected error has occurred',
            args={'code': camel_to_upper(e.__class__.__name__)},
        ) from e

    if check_cache and cache_key:
        results['args']['cache_key'] = cache_key
        if 'cache_time' not in results['args']:
            logger.debug(
                'Results generated with \'cache_key\'. Calling \'_set_cache\'.'
            )
            results['args']['cache_time'] = datetime.datetime.utcnow().isoformat()
        asyncio.create_task(_set_cache(func=func, cache_key=cache_key, results=results))

    return results


def _process_query_mod(
    *,
    query: 'Query',
    query_mod: Union[
        MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]
    ],
    env: 'NawahEnv',
    doc: 'NawahDoc',
    append_mod: bool = False,
):
    if not query_mod:
        return

    if isinstance(query_mod, list):
        for query_mod_child in query_mod:
            _process_query_mod(query=query, query_mod=query_mod_child, env=env, doc=doc)

    elif isinstance(query_mod, dict):
        for attr_name, attr_val in query_mod.items():
            if isinstance(attr_val, (list, dict)):
                _process_query_mod(query=query, query_mod=attr_val, env=env, doc=doc)
            elif isinstance(attr_val, Var):
                if attr_val.type not in [VarType.SESSION, VarType.CONFIG]:
                    raise Exception(
                        f'\'query_mod\' attr \'{attr_name}\' is of invalid Var type '
                        f'\'{attr_val.type}\''
                    )

                query_mod[attr_name] = var_value(attr_val, env=env, doc=doc)

    if append_mod:
        query.append(query_mod)


def _process_doc_mod(
    *,
    doc: 'NawahDoc',
    doc_mod: Union[MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]],
    env: 'NawahEnv',
    query: 'Query',
    append_mod: bool = False,
):
    if not doc_mod:
        return

    if isinstance(doc_mod, list):
        for doc_mod_child in doc_mod:
            _process_doc_mod(doc=doc, doc_mod=doc_mod_child, env=env, query=query)

    elif isinstance(doc_mod, dict):
        for attr_name, attr_val in doc_mod.items():
            if isinstance(attr_val, (list, dict)):
                _process_doc_mod(doc=doc, doc_mod=attr_val, env=env, query=query)
            elif isinstance(attr_val, Var):
                if attr_val.type not in [VarType.SESSION, VarType.CONFIG]:
                    raise Exception(
                        f'\'doc_mod\' attr \'{attr_name}\' is of invalid Var type '
                        f'\'{attr_val.type}\''
                    )

                doc_mod[attr_name] = var_value(attr_val, env=env, doc=doc)

    if append_mod:
        doc_mod = cast(MutableMapping, doc_mod)
        doc.update(doc_mod)


def _check_query_attrs(
    *,
    query: 'Query',
    query_attrs: MutableSequence[MutableMapping[str, 'Attr']],
):
    if not query_attrs:
        return

    for query_attrs_set in query_attrs:
        for attr_name, attr_type in query_attrs_set.items():
            if attr_name not in query:
                raise MissingQueryAttrException(attr_name=attr_name)

            for i, attr_val in enumerate(query[attr_name]):
                try:
                    query[attr_name][i] = validate_attr(
                        mode='create',
                        attr_name=attr_name,
                        attr_type=attr_type,
                        attr_val=attr_val,
                    )
                except InvalidAttrException as e:
                    raise InvalidQueryAttrException(
                        attr_name=attr_name,
                        attr_type=attr_type,
                        val_type=type(attr_val),
                    ) from e


def _check_doc_attrs(
    *,
    doc: 'NawahDoc',
    doc_attrs: MutableSequence[MutableMapping[str, 'Attr']],
):
    if not doc_attrs:
        return

    for doc_attrs_set in doc_attrs:
        for attr_name, attr_type in doc_attrs_set.items():
            if attr_name not in doc:
                raise MissingDocAttrException(attr_name=attr_name)

            try:
                doc[attr_name] = validate_attr(
                    mode='create',
                    attr_name=attr_name,
                    attr_type=attr_type,
                    attr_val=doc[attr_name],
                )
            except InvalidAttrException as e:
                raise InvalidDocAttrException(
                    attr_name=attr_name,
                    attr_type=attr_type,
                    val_type=type(doc[attr_name]),
                ) from e
