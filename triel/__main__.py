import sys
from runpy import run_path

from triel import manage


def main():
    sys.argv = ['', 'runserver', *sys.argv[1:]]
    run_path(manage.__file__, run_name="__main__")


if __name__ == '__main__':
    main()
