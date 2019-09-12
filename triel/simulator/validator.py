import subprocess

from rest_framework import serializers

GHDL_NAME = 'ghdl'
GHDL_EXE = 'ghdl'
GHDL_ARGS = ("--version")


def validate_simulator(name, path):
    if name == GHDL_NAME:
        return validate_ghdl(path)


def validate_ghdl(path):
    result = False
    try:
        if not path:
            path = GHDL_EXE
        output = subprocess.check_output([path, *GHDL_ARGS]).decode()
        result = GHDL_NAME in output
    except FileNotFoundError:
        pass

    if not result:
        raise serializers.ValidationError('The path for GHDL is not valid.')
