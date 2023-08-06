
import sys
from collections import defaultdict

from .pypi_project import pypi


def _check_pypi(package_name: str):
    try:
        if pypi.is_project(package_name):
            return 'found'
        return 'not-found'
    except Exception as error:
        print(error, file=sys.stderr)
        return 'error'


def check_pypi(package_name: str):
    PYTHON_2_SYS = defaultdict(lambda: 2, **{
        'found': 0,
        'not-found': 1,
        'error': 2,
    })
    sys.exit(PYTHON_2_SYS[_check_pypi(package_name)])


def main():
    check_pypi(sys.argv[1])


if __name__ == '__main__':
    main()
