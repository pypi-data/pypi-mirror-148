'''Provides 'setting' Module Functions callables'''

from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import FuncException, InvalidAttrException
from nawah.utils import call, decode_attr_type, validate_doc


async def _create(env, doc):
    create_results = await call('base/create', module_name='setting', env=env, doc=doc)

    if create_results['status'] != 200:
        return create_results

    if doc['type'] in ['user', 'user_sys']:
        if (
            doc['user'] == env['session']['user']['_id']
            and doc['var'] in Config.user_doc_settings
        ):
            env['session']['user'][doc['var']] = doc['val']

    return create_results


async def _update(env, query, doc):
    for attr in doc.keys():
        if attr == 'val' or attr.startswith('val.'):
            val_attr = attr
            break
    else:
        raise FuncException(
            status=400,
            msg='Could not match doc with any of the required doc_args. Failed sets: '
            '[\'val\': Missing]',
            args={'code': 'INVALID_DOC'},
        )

    setting_results = await call(
        'setting/read',
        skip_events=[Event.PERM],
        env=env,
        query=query,
    )
    if not setting_results['args']['count']:
        raise FuncException(
            status=400, msg='Invalid Setting doc', args={'code': 'INVALID_SETTING'}
        )

    setting = setting_results['args']['docs'][0]
    # [DOC] Attempt to validate val against Setting val_type
    try:
        exception_raised: Exception = None
        setting_val_type = decode_attr_type(encoded_attr_type=setting['val_type'])
        await validate_doc(
            mode='update',
            doc=doc,
            attrs={'val': setting_val_type},
        )
    except InvalidAttrException as e:
        exception_raised = e

    if exception_raised or doc[val_attr] is None:
        raise FuncException(
            status=400,
            msg=f'Invalid value for for Setting doc of type \'{type(doc[val_attr])}\' with '
            f'required type \'{setting["val_type"]}\'',
            args={'code': 'INVALID_ATTR'},
        )

    create_results = await call('base/create', module_name='setting', env=env, doc=doc)

    if create_results['status'] != 200:
        return create_results

    if doc['type'] in ['user', 'user_sys']:
        if (
            doc['user'] == env['session']['user']['_id']
            and doc['var'] in Config.user_doc_settings
        ):
            env['session']['user'][doc['var']] = doc['val']

    return create_results
