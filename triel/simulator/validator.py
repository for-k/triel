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

import subprocess

from rest_framework import serializers

from triel.server.manager.models.master_enuml import SimulatorNames

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
