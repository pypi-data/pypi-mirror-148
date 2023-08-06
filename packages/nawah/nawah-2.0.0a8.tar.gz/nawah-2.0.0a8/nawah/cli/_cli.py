'''Provides function to create CLI for Nawah'''

import argparse

from nawah import __version__

from ._create import create


def cli():
    '''Creates CLI for Nawah'''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        help='Print Nawah version and exit',
        action='version',
        version=f'Nawah v{__version__}',
    )

    subparsers = parser.add_subparsers(
        title='Command',
        description='Nawah CLI command to run',
        dest='command',
    )

    parser_create = subparsers.add_parser('create', help='Create new Nawah app')
    parser_create.set_defaults(func=create)
    parser_create.add_argument(
        'component',
        help='Name of the app to create',
        choices=['app', 'package', 'module'],
    )
    parser_create.add_argument(
        'name',
        type=str,
        help='Name of component to create',
    )
    parser_create.add_argument(
        'path',
        type=str,
        nargs='?',
        help='Path to Nawah app [default .]',
        default='.',
    )
    parser_create.add_argument(
        '--package',
        type=str,
        nargs='?',
        help='Name of package in app to create the module in. Required when Nawah app folder '
        'includes multiple packages',
        default=None,
    )

    args = parser.parse_args()

    if args.command:
        args.func(args)

    else:
        parser.print_help()
