'''Provides exceptions related to Nawah Function'''

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import ResultsArgs


class FuncException(Exception):
    '''Raised by \'call\' Utility when encounters an exception raised
    by Nawah Function callable'''

    def __init__(self, *, status: int, msg: str, args: 'ResultsArgs'):
        super().__init__(msg, {'status': status, 'args': args})


class MissingQueryAttrException(Exception):
    '''Raied by '_check_query_attrs' if 'attr_name' is missing from checked Query object'''

    status = 400

    def __init__(self, *, attr_name):
        super().__init__(
            MissingQueryAttrException.format_msg(attr_name=attr_name),
            {'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, attr_name):
        '''Formats exception message'''

        return f'Missing attr \'{attr_name}\' from Query'


class InvalidQueryAttrException(Exception):
    '''Raised by '_check_query_attrs' if 'attr' has invalid value'''

    status = 400

    def __init__(self, *, attr_name, attr_type, val_type):
        super().__init__(
            InvalidQueryAttrException.format_msg(
                attr_name=attr_name, attr_type=attr_type, val_type=val_type
            ),
            {'attr_name': attr_name, 'attr_type': attr_type, 'val_type': val_type},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_type, val_type):
        '''Formats exception message'''

        return (
            f'Invalid attr \'{attr_name}\' of type \'{val_type}\' with required type '
            f'\'{attr_type}\''
        )


class MissingDocAttrException(Exception):
    '''Raied by '_check_query_attrs' if 'attr_name' is missing from checked Doc object'''

    status = 400

    def __init__(self, *, attr_name):
        super().__init__(
            MissingDocAttrException.format_msg(attr_name=attr_name),
            {'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, attr_name):
        '''Formats exception message'''

        return f'Missing attr \'{attr_name}\' from Doc'


class InvalidDocAttrException(Exception):
    '''Raised by '_check_doc_attrs' if 'attr' has invalid value'''

    status = 400

    def __init__(self, *, attr_name, attr_type, val_type):
        super().__init__(
            InvalidDocAttrException.format_msg(
                attr_name=attr_name, attr_type=attr_type, val_type=val_type
            ),
            {'attr_name': attr_name, 'attr_type': attr_type, 'val_type': val_type},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_type, val_type):
        '''Formats exception message'''

        return (
            f'Invalid attr \'{attr_name}\' of type \'{val_type}\' with required type '
            f'\'{attr_type}\''
        )
