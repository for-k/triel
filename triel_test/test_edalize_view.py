import unittest

import requests

from triel_test.test_master_view import TrielTestCase, TRIEL_URL

TEST_URL = TRIEL_URL + 'tests/'


class Edalize(TrielTestCase):
    def test_ghdl(self):
        data = {
            "name": "test_ghdl",
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "files": [
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd",
                 "file_type": "vhdlSource-2008"},
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder_tb.vhd",
                 "file_type": "vhdlSource-2008"}
            ],
            "top_level": "adder_tb",
            "tool": "ghdl",
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


if __name__ == '__main__':
    unittest.main()
