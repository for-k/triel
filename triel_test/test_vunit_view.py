import unittest

import requests

from triel.server.manager.models.master_enuml import SimulatorNames, SuiteNames
from triel.server.manager.models.test_enum import FileTypeChoices
from triel_test.resources_test import resource_test_path
from triel_test.test_master_view import TrielTestCase, TRIEL_URL

TEST_URL = TRIEL_URL + 'tests/'


class VUnit(TrielTestCase):
    def test_ghdl(self):
        data = {
            "suite": SuiteNames.VUNIT.value,
            "working_dir": resource_test_path("vunit"),
            "files": [
                {"name": resource_test_path("vunit/run.py"),
                 "file_type": FileTypeChoices.py.value},
            ],
            "tool": SimulatorNames.GHDL.value,
        }
        response = requests.post(TEST_URL, json=data)
        self.print_response(response)
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
