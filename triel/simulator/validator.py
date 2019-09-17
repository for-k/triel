import subprocess
from enum import Enum

from rest_framework import serializers


class LanguageNames(Enum):
    VHDL = "vhdl"
    VERILOG = "verilog"


class SimulatorNames(Enum):
    GHDL = 'ghdl'
    ICARUS = 'icarus'


EXE = {
    SimulatorNames.GHDL.value: 'ghdl',
    SimulatorNames.ICARUS.value: 'iverilog'
}

ARGS = {
    SimulatorNames.GHDL.value: '--version',
    SimulatorNames.ICARUS.value: '-v'
}

VALIDATION = {
    SimulatorNames.GHDL.value: 'ghdl',
    SimulatorNames.ICARUS.value: 'Icarus Verilog'
}


def validate_simulator(name, path):
    result = False
    try:
        if not path:
            path = EXE.get(name)
        output = subprocess.check_output([path, ARGS.get(name)]).decode()
        result = VALIDATION.get(name) in output
    except FileNotFoundError:
        pass

    if not result:
        raise serializers.ValidationError(f'The path for {name} is not valid.')
