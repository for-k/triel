from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='triel',
    version='0.2.0',
    description='Teros Simulator Manager',
    long_description=long_description,
    url='www.terostech.com',
    author='Teros Technology',
    author_email='info@terostech.com',
    license='GNU General Public License (GPL)',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='teros fpga',

    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'triel = triel.__main__:main',
        ],
    },

    packages=find_packages(exclude=["*_test", "*_tests"]),
    include_package_data=True,
    install_requires=[
        "edalize < 1",
        "vunit_hdl < 5"
    ],
)