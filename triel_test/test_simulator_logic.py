"""

 Copyright 2020 Teros Technology

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
 along with Colibri.  If not, see <https://www.gnu.org/licenses/>.

"""

import unittest

from triel.simulator.validator import validate_simulator


class SimulatorPathValidator(unittest.TestCase):
    def test_ghdl(self):
        validate_simulator('ghdl', 'ghdl')
        assert True

    def test_icarus(self):
        validate_simulator('icarus', 'iverilog')


if __name__ == '__main__':
    unittest.main()
