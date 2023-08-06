'''Provides 'create' Base Function callable'''

import datetime
import logging
from typing import TYPE_CHECKING, Any, MutableSequence, cast

import nawah.data as Data
from nawah.config import Config
from nawah.enums import Event
from nawah.utils import call, expand_val, validate_doc

from .exceptions import (DuplicateUniqueException,
                         UtilityModuleDataCallException)

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results

logger = logging.getLogger('nawah')


async def create(
    *,
    module_name: str,
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    doc: 'NawahDoc',
) -> 'Results':
    '''Creates doc for a module'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='create'
        )

    # Expand dot-notated keys onto dicts
    doc = expand_val(doc=doc)
    # Deleted all extra doc args
    doc = {
        attr: doc[attr]
        for attr in ['_id', *module.attrs]
        if attr in doc and doc[attr] is not None
    }
    # Append host_add, user_agent, create_time, if present in attrs
    if (
        'user' in module.attrs
        and 'host_add' not in doc
        and env['session']
        and Event.ATTRS not in skip_events
    ):
        doc['user'] = env['session']['user']['_id']
    if 'create_time' in module.attrs:
        doc['create_time'] = datetime.datetime.utcnow().isoformat()
    if 'host_add' in module.attrs and 'host_add' not in doc:
        doc['host_add'] = env['REMOTE_ADDR']
    if 'user_agent' in module.attrs and 'user_agent' not in doc:
        doc['user_agent'] = env['HTTP_USER_AGENT']
    if Event.ATTRS not in skip_events:
        # Check presence and validate all attrs in doc args
        validate_doc(
            mode='create',
            doc=doc,
            attrs=module.attrs,
        )
        # Check unique_attrs
        if module.unique_attrs:
            unique_attrs_query: MutableSequence[Any] = [[]]
            for attr in module.unique_attrs:
                if isinstance(attr, str):
                    attr = cast(str, attr)
                    unique_attrs_query[0].append({attr: doc[attr]})
                elif isinstance(attr, tuple):
                    unique_attrs_query[0].append(
                        {child_attr: doc[child_attr] for child_attr in attr}
                    )
                # [TODO] Implement use of single-item dict with LITERAL Attr Type for dynamic unique check based on doc value
            unique_attrs_query.append({'$limit': 1})
            unique_results = await call(
                'base/read',
                module_name=module_name,
                skip_events=[Event.PERM],
                env=env,
                query=unique_attrs_query,
            )
            if unique_results['args']['count']:
                raise DuplicateUniqueException(unique_attrs=module.unique_attrs)
    # Execute Data driver create
    results = await Data.create(env=env, collection_name=module.collection, doc=doc)

    # create soft action is to only return the new created doc _id.
    if Event.SOFT in skip_events:
        read_results = await call(
            'base/read',
            module_name=module_name,
            skip_events=[Event.PERM],
            env=env,
            query=[[{'_id': results['docs'][0]}]],
        )
        results = read_results['args']

    return {'status': 200, 'msg': f'Created {results["count"]} docs.', 'args': results}
