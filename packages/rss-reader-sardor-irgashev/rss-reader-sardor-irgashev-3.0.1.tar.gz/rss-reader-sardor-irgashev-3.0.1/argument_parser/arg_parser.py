"""The module provides necessary functions to parse and handle command-line arguments"""

import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from datetime import datetime

from _version import __version__

logger = logging.getLogger()


def positive_int(value: str) -> int:
    """Checks whether the provided argument is positive integer

    Args:
        value: Command-line-provided argument

    Returns:
        Integer representation of the provided argument

    Raises:
        ArgumentTypeError: If provided integer value is less than 0
    """
    try:
        int_val = int(value)
        if int_val <= 0:
            raise ArgumentTypeError('Limit can take positive integer value only! Program terminated. Try again.')
        return int_val
    except (ValueError, TypeError):
        sys.exit('Limit can take integer value only! Program terminated. Try again.')


def valid_date(date: str) -> str:
    """Checks whether the provided argument is a valid date
    Args:
        date: Command-line-provided argument

    Returns:
        str corresponding to 'date', parsed according to format provided

    Raises:
        ArgumentTypeError: If provided 'date' and format cannot be parsed
    """
    try:
        return datetime.strptime(date, "%Y%m%d").strftime("%Y%m%d")
    except ValueError:
        raise ArgumentTypeError('Argument is outside of defined ranges. Program terminated. Try again.')


def handle_args() -> Namespace:
    """Parses command-line arguments

    Returns:
        Argument-attributes-populated namespace
    """
    parser = ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument('source', nargs='?', default='', help='RSS URL')
    parser.add_argument('--version', action='version', version=f'Version {__version__}', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=positive_int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=valid_date, help='News publishing date')

    return parser.parse_args()
