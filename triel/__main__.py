import sys
from runpy import run_path

from triel import manage

if __name__ == '__main__':
    sys.argv = ['', 'runserver', *sys.argv[1:]]
    run_path(manage.__file__, run_name="__main__")
