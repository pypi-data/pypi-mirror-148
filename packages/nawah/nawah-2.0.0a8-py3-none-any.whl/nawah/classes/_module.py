'''Provides 'Module' dataclass'''

from dataclasses import dataclass
from typing import (TYPE_CHECKING, MutableMapping, MutableSequence, Optional,
                    Tuple, Union)

if TYPE_CHECKING:
    from ._attr import Attr
    from ._counter import Counter
    from ._default import Default
    from ._diff import Diff
    from ._extn import Extn
    from ._func import Func


@dataclass(kw_only=True)
class Module:
    '''Module dataclass serves role of defining a Nawah Datatype along the
    funcs required for it. It is at the centre of Nawah, as in, any call
    in Nawah is directed to a specific Module and fulfilled by one of its
    defined funcs, completed with other configurations defined.'''

    # pylint: disable=too-many-instance-attributes

    desc: Optional[str]
    collection: str
    attrs: MutableMapping[str, 'Attr']
    funcs: MutableMapping[str, 'Func']
    unique_attrs: MutableSequence[Union[Tuple[str], str]]
    counters: MutableMapping[str, 'Counter']
    diff: Optional['Diff']
    create_draft: bool
    update_draft: bool
    defaults: MutableMapping[str, 'Default']
    extns: MutableMapping[str, 'Extn']
    privileges: MutableSequence[str]
    name: Optional[str] = None

    def __post_init__(self):
        # Force setting name to None
        self.name = None
