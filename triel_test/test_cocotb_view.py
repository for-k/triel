import unittest

import requests

from triel_test.test_master_view import TrielTestCase, TRIEL_TEST_URL

COCO_URL = TRIEL_TEST_URL + 'coco/'


class Coco(TrielTestCase):
    def test_adder_vlog(self):
        data = {
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "modules": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py"}],
            "sources": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.v"}],
            "top_level": "adder",
            "simulator": "icarus",
            "simulator_args": [{"argument": "--vcd", "value": "func.vcd"}],
        }
        response = requests.post(COCO_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201

    def test_adder_vhdl(self):
        data = {
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "modules": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py"}],
            "sources": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd"}],
            "top_level": "adder",
            "simulator": "ghdl",
            "simulator_args": [{"argument": "--vcd", "value": "func.vcd"}],
        }
        response = requests.post(COCO_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
