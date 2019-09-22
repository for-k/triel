import unittest

import requests

from triel_test.test_master_view import TrielTestCase, TRIEL_TEST_URL

EDALIZE_URL = TRIEL_TEST_URL + 'edalize/'


class Edalize(TrielTestCase):
    def test_ghdl(self):
        data = {
            "name": "test_ghdl",
            "working_dir": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple",
            "sources": [{"path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd"},
                        {"path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder_tb.vhd"}],
            "top_level": "adder_tb",
            "simulator": "ghdl",
            "simulator_args": [{"group": "analyze_options", "argument": "-fexplicit"},
                               {"group": "analyze_options", "argument": "--no-vital-checks"},
                               {"group": "analyze_options", "argument": "-frelaxed-rules"},
                               {"group": "run_options", "argument": "--disp-time"}],
        }
        response = requests.post(EDALIZE_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
