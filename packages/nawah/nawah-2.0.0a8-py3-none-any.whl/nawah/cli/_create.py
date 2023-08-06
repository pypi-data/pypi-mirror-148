import argparse
import logging
import os
import re

logger = logging.getLogger('nawah')

NAME_PATTERN = r'^[a-z][a-z0-9_]+$'


def create(args: argparse.Namespace):
    '''Provides create command functionality to Nawah CLI'''

    if not re.match(r'^[a-z][a-z0-9_]+$', args.name):
        raise Exception(
            'Value for \'name\' CLI Arg is invalid. Name should have only small letters, '
            'numbers, and underscores.'
        )

    component = args.component
    path = os.path.realpath(args.path)

    logger.info(
        'Checking possibility to create component \'%s\', at \'%s\'', component, path
    )
