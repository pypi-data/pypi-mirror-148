import argparse
import sys

from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available

from mutil.util import get_util
from mutil.version import current_version

MUTIL_USAGE = """Usage
> mutil <platform>
"""


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'platform',
        help='What platform would you like to get util for?',
    )
    return parser


def main() -> int:
    try:
        check_new_update_available(
            package_name='mosaicml-mutil',
            current_version=current_version,
        )
    except NeedsUpdateError:
        return 1

    parser = get_parser()
    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_usage()
        return 1

    return get_util(platform=args.platform)


if __name__ == "__main__":
    sys.exit(main())
