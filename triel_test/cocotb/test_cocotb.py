import unittest

import requests


class Coco(unittest.TestCase):
    def test_adder(self):
        url = 'http://127.0.0.1:8000/coco/'
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
        response = requests.post(url, json=data)
        print(response.status_code)
        print(response.json())


if __name__ == '__main__':
    unittest.main()
