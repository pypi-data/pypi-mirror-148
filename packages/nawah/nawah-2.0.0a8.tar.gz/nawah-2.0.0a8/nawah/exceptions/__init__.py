'''Provides exceptions used in Nawah'''

from ._attr import (InvalidAttrTypeArgException, InvalidAttrTypeException,
                    InvalidAttrTypeRefException, JSONPathNotFoundException)
from ._call import (InvalidCallEndpointException, InvalidFuncException,
                    InvalidModuleException, NotPermittedException)
from ._config import ConfigException
from ._data import UnknownDeleteStrategyException
from ._func import (FuncException, InvalidDocAttrException,
                    InvalidQueryAttrException, MissingDocAttrException,
                    MissingQueryAttrException)
from ._query import (InvalidQueryArgException, InvalidQueryException,
                     UnknownQueryArgException)
from ._validate import InvalidAttrException, MissingAttrException
from ._var import InvalidLocaleException, InvalidVarException

__all__ = [
    'InvalidAttrTypeArgException',
    'InvalidAttrTypeException',
    'InvalidAttrTypeRefException',
    'JSONPathNotFoundException',
    'InvalidCallEndpointException',
    'InvalidFuncException',
    'InvalidModuleException',
    'NotPermittedException',
    'ConfigException',
    'UnknownDeleteStrategyException',
    'FuncException',
    'InvalidDocAttrException',
    'InvalidQueryAttrException',
    'MissingDocAttrException',
    'MissingQueryAttrException',
    'InvalidQueryArgException',
    'InvalidQueryException',
    'UnknownQueryArgException',
    'InvalidAttrException',
    'MissingAttrException',
    'InvalidLocaleException',
    'InvalidVarException',
]
