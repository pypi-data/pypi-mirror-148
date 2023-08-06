'''Provides 'delete_lock' Base Function callable'''

import logging
from typing import TYPE_CHECKING

import nawah.data as Data
from nawah.config import Config
from nawah.enums import DeleteStrategy

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, Results

logger = logging.getLogger('nawah')


async def delete_lock(
    *, module_name: str, env: 'NawahEnv', query: 'Query'
) -> 'Results':
    '''Deletes locks for a module matching query \'query\'. If not, raises MethodException.'''

    module = Config.modules[module_name]

    docs_results = results = await Data.read(
        env=env,
        collection_name=f'{module.collection}__lock',
        attrs={},
        query=query,
        skip_process=True,
    )
    results = await Data.delete(
        env=env,
        collection_name=f'{module.collection}__lock',
        docs=[doc['_id'] for doc in docs_results['docs']],
        strategy=DeleteStrategy.FORCE_SYS,
    )

    return {
        'status': 200,
        'msg': f'Deleted {results["count"]} docs.',
        'args': results,
    }
