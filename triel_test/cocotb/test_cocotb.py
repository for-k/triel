import unittest

import requests

COCO_URL = 'http://127.0.0.1:8000/coco/'


class Coco(unittest.TestCase):
    def test_adder_vlog(self):
        data = {
            "name": "test_adder_vlog",
            "top_level": "adder",
            "simulator": 2,
            "language": 2,
            "module": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py",
            "files": [
                {
                    "path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.v"
                }
            ]
        }
        response = requests.post(COCO_URL, json=data)
        print(response.status_code)
        print(response.json())

        assert response.status_code == 201

    def test_adder_vhdl(self):
        data = {
            "name": "test_adder_vhdl",
            "top_level": "adder",
            "simulator": 1,
            "language": 1,
            "module": "/mnt/data/Programacion/teros/triel/triel_test/scripts/cocotb/simple/test_adder.py",
            "files": [
                {
                    "path": "/mnt/data/Programacion/teros/triel/triel_test/hdl/adder.vhd"
                }
            ]
        }
        response = requests.post(COCO_URL, json=data)
        print(response.status_code)
        print(response.json())

        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
