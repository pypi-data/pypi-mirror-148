'''Provides 'Job' dataclass'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    from croniter import croniter

    from nawah.types import NawahEnv


@dataclass(kw_only=True)
class Job:
    '''Job dataclass serves role of defining items of 'jobs' Config Attr which
    are callabled, called periodically per cron-based schedule'''

    job: 'JobCallable'
    schedule: str
    prevent_disable: bool
    _cron_schedule: 'croniter'
    _next_time: Optional[str] = None
    _disabled: bool = False


class JobCallable(Protocol):
    '''Provides type-hint for 'job' callable of 'Job' '''

    # pylint: disable=too-few-public-methods
    def __call__(
        self,
        env: 'NawahEnv',
    ) -> None:
        ...
