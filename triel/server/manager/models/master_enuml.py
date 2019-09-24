from enum import Enum


class LanguageNames(Enum):
    VHDL = "vhdl"
    VERILOG = "verilog"


class SimulatorNames(Enum):
    GHDL = 'ghdl'
    ICARUS = 'icarus'


class SuiteNames(Enum):
    COCOTB = 'cocotb'
    EDALIZE = 'edalize'
    VUNIT = 'vunit'
