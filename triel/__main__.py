"""

 Copyright 2021 Teros Technology

 Ismael Perez Rojo
 Carlos Alberto Ruiz Naranjo
 Alfredo Saez

 This file is part of Triel.

 Triel is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Triel is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Triel.  If not, see <https://www.gnu.org/licenses/>.

"""
from argparse import ArgumentParser

from triel.graph import EdalizeGraphDependency
from triel.server import TrielServer
from triel.simulation import EdalizeLauncher

DEFAULT_PORT = 8472


def argument_parser():
    parser = ArgumentParser(description="Triel")
    parser.add_argument(
        "-p", "--port", type=int, help="Server port", default=DEFAULT_PORT,
    )
    return parser.parse_args()


def main():
    # Read input parameters
    args = argument_parser()
    # Activate services
    EdalizeGraphDependency()
    EdalizeLauncher()
    # Launch Server listener
    TrielServer(args.port)


if __name__ == "__main__":
    main()
