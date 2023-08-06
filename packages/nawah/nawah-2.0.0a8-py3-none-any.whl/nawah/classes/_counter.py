'''Provides 'Counter' dataclass'''

from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(kw_only=True)
class Counter:
    '''Counter dataclass serves role as Counter Value Instruction'''

    pattern_formatter: 'CounterPatternFormatter'
    counter: Optional[str] = None


class CounterPatternFormatter(Protocol):
    '''Provides type-hint for 'pattern_formatter' callable of 'Counter' '''

    # pylint: disable=too-few-public-methods

    def __call__(
        self,
        counter_value: str,
    ) -> str:
        ...
