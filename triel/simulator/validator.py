import subprocess

from rest_framework import serializers

from triel.server.manager.models.master_model import SimulatorNames

EXE = {
    SimulatorNames.GHDL.value: 'ghdl',
    SimulatorNames.ICARUS.value: 'iverilog'
}

ARGS = {
    SimulatorNames.GHDL.value: '--version',
    SimulatorNames.ICARUS.value: '-h'
}

VALIDATION = {
    SimulatorNames.GHDL.value: 'GHDL',
    SimulatorNames.ICARUS.value: 'Usage: iverilog'
}


def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()


def validate_simulator(name, path):
    result = False
    try:
        if not path:
            path = EXE.get(name)
        error_code, stdout, stderr = run([path, ARGS.get(name)])
        result = VALIDATION.get(name) in stdout + stderr
    except FileNotFoundError:
        pass

    if not result:
        raise serializers.ValidationError(f'The path for {name} is not valid.')
