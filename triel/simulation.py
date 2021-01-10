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
import logging
import os
import shutil
from subprocess import Popen, PIPE, STDOUT
from typing import Dict
from unittest.mock import patch

import edalize

from triel.broker import Broker
from triel.topic import SimulationConsumer, TrielTopic

WORK_DIRECTORY = "work_directory"
TOOL_OPTIONS = "tool_options"


def check_call_patched(sim_id: int, *popenargs, **kwargs):
    p = Popen(*popenargs, **kwargs, stdout=PIPE, stderr=STDOUT)
    while p.returncode is not None:
        for line in p.stdout:
            Broker.produce(TrielTopic.SIMULATION_STDOUT, (sim_id, line))
    return p.returncode


def search_for_wave_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".vcd"):
                return os.path.join(folder, file)
        for dir in dirs:
            search_for_wave_files(os.path.join(folder, dir))
    return ""


class EdalizeLauncher(SimulationConsumer):
    def __init__(self):
        super().__init__()
        self.sim_id: int = 0

    def on_simulation_requested(self, tedam_json: Dict):
        self.sim_id += 1

        work_root = os.path.join(tedam_json.pop(WORK_DIRECTORY), "build")
        self.clean_build(work_root)

        tool = tuple(tedam_json.get(TOOL_OPTIONS, {}).keys())[0]

        backend = edalize.get_edatool(tool)(edam=tedam_json, work_root=work_root)
        os.makedirs(work_root)

        Broker.produce(
            TrielTopic.SIMULATION_STARTED_RES,
            {"sim_id": self.sim_id},
        )

        with patch("edalize.edatool.subprocess.check_call") as check_call_mock:
            try:
                check_call_mock.side_effect = (
                    lambda *popenargs, **kwargs: check_call_patched(
                        self.sim_id, *popenargs, **kwargs
                    )
                )
                backend.configure()
                backend.build()
                backend.run()
            except Exception as err:
                logging.exception(err)
            finally:
                result = {
                    "summary": {
                        "test": 1,
                        "failures": "---",
                        "errors": "---",
                        "skipped": "--",
                    },
                    "test": [
                        {
                            "classname": "Edalize",
                            "name": "---",
                            "time": "---",
                            "test": "---",
                            "waveform": search_for_wave_files(work_root),
                        }
                    ],
                }
                Broker.produce(
                    TrielTopic.SIMULATION_FINISHED_RES,
                    {"sim_id": self.sim_id, "result": result},
                )

    def on_cancel_simulation(self, sim_id: int):
        # TODO
        pass

    @staticmethod
    def clean_build(build_dir: str):
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
