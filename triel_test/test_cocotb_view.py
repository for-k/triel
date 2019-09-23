import unittest

import requests

from triel_test.test_master_view import TrielTestCase, TRIEL_URL

COCO_URL = TRIEL_URL + 'tests/'


class Coco(TrielTestCase):
    def test_adder_vlog(self):
        data = {
            "suite": "cocotb",
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "files": [
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py",
                 "file_type": "py"},
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.v",
                 "file_type": "verilogSource-2005"}
            ],
            "top_level": "adder",
            "tool": "icarus",
            "tool_options": [
                {"group": "--vcd", "argument": "func.vcd"}
            ]
        }
        response = requests.post(COCO_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201

    def test_adder_vhdl(self):
        data = {
            "suite": "cocotb",
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "files": [
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py",
                 "file_type": "py"},
                {"name": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd",
                 "file_type": "vhdlSource-2008"}
            ],
            "top_level": "adder",
            "tool": "ghdl",
            "tool_options": [
                {"group": "--vcd", "argument": "func.vcd"}
            ]
        }
        response = requests.post(COCO_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
