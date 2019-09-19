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
