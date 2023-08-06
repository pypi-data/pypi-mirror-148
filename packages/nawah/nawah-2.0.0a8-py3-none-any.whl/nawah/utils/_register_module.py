'''Provides 'register_module' Utility'''

from typing import (TYPE_CHECKING, Callable, MutableMapping, MutableSequence,
                    Optional, Tuple, Union)

from nawah.classes import Module

if TYPE_CHECKING:
    from nawah.classes import Attr, Counter, Default, Diff, Extn, Func


def register_module(
    name,
    /,
    *,
    funcs: MutableMapping[str, 'Func'],
    collection: str = None,
    attrs: MutableMapping[str, 'Attr'] = None,
    unique_attrs: Optional[MutableSequence[Union[Tuple[str, ...], str]]] = None,
    counters: MutableMapping[str, 'Counter'] = None,
    diff: 'Diff' = None,
    create_draft: bool = False,
    update_draft: bool = False,
    defaults: MutableMapping[str, 'Default'] = None,
    extns: MutableMapping[str, 'Extn'] = None,
    privileges: MutableSequence[str] = None,
    desc: Optional[str] = None,
) -> Callable[[], Tuple[str, 'Module']]:
    '''Returns callable that is used as item for 'modules' Package Config Attr'''

    def _():
        return (
            name,
            Module(
                desc=desc,
                collection=collection,
                attrs=attrs or {},
                funcs=funcs,
                counters=counters or {},
                unique_attrs=unique_attrs or [],
                diff=diff,
                create_draft=create_draft,
                update_draft=update_draft,
                defaults=defaults or {},
                extns=extns or {},
                privileges=privileges
                or ['admin', 'read', 'create', 'update', 'delete'],
            ),
        )

    return _
