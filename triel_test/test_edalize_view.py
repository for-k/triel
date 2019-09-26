import unittest

import requests

from triel.server.manager.models.master_enuml import SimulatorNames
from triel.server.manager.models.test_enum import FileTypeChoices
from triel_test.resources_test import resource_test_path
from triel_test.test_master_view import TrielTestCase, TRIEL_URL

TEST_URL = TRIEL_URL + 'tests/'


class Edalize(TrielTestCase):
    def test_ghdl(self):
        data = {
            "name": "test_ghdl",
            "working_dir": resource_test_path("hdl"),
            "files": [
                {"name": resource_test_path("hdl/adder.vhd"),
                 "file_type": FileTypeChoices.vhdl08.value},
                {"name": resource_test_path("hdl/adder_tb.vhd"),
                 "file_type": FileTypeChoices.vhdl08.value}
            ],
            "top_level": "adder_tb",
            "tool": SimulatorNames.GHDL.value,
            "tool_options": [
                {"group": "analyze_options", "argument": "-fexplicit"},
                {"group": "analyze_options", "argument": "--no-vital-checks"},
                {"group": "analyze_options", "argument": "-frelaxed-rules"},
                {"group": "run_options", "argument": "--disp-time"}
            ]
        }
        response = requests.post(TEST_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201

    def test_icarus(self):
        data = {
            "name": "test_icarus",
            "working_dir": resource_test_path("hdl"),
            "files": [
                {"name": resource_test_path("hdl/basic_and.v"),
                 "file_type": FileTypeChoices.vlog05.value},
                {"name": resource_test_path("hdl/basic_and_tb.v"),
                 "file_type": FileTypeChoices.vlog05.value}
            ],
            "top_level": "basic_and_tb",
            "tool": SimulatorNames.ICARUS.value,
        }
        response = requests.post(TEST_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
