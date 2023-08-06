'''Provides 'Cache' dataclass'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Protocol

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, NawahEvents


@dataclass(kw_only=True)
class Cache:
    '''Cache dataclass serves role of defining Cache Instruction, which
    instructs Nawah of when to cache call results'''

    channel: str
    condition: 'CacheCondition'
    user_scoped: bool
    period: Optional[int] = None

    def __post_init__(self):
        Config.sys.cache_channels.add(self.channel)


class CacheCondition(Protocol):
    '''Provides type-hint for 'condition' callable of 'Cache' '''

    # pylint: disable=too-few-public-methods

    def __call__(
        self,
        skip_events: 'NawahEvents',
        env: 'NawahEnv',
        query: 'Query',
    ) -> bool:
        ...
