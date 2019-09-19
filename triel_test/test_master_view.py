import unittest

import requests

TRIEL_TEST_URL = "http://localhost:8000/"
LANGUAGE_URL = TRIEL_TEST_URL + 'languages/'
SIMULATOR_URL = TRIEL_TEST_URL + 'simulators/'
SUITE_URL = TRIEL_TEST_URL + 'suites/'


class TrielTestCase(unittest.TestCase):
    def setUp(self) -> None:
        print('\n\n' + "----------- " + self._testMethodName + " -----------")

    @staticmethod
    def print_response(response):
        print(response.status_code)
        print(response.json())


class LanguageCase(TrielTestCase):

    def test_list_languages(self):
        response = requests.get(LANGUAGE_URL)
        self.print_response(response)
        assert response.status_code == 200

    def test_get_languages(self):
        response = requests.get(LANGUAGE_URL + '1/')
        self.print_response(response)
        assert response.status_code == 200

    def test_post_languages(self):
        response = requests.post(LANGUAGE_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 405

    def test_patch_languages(self):
        response = requests.patch(LANGUAGE_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 405

    def test_delete_languages(self):
        response = requests.delete(LANGUAGE_URL + '1/')
        self.print_response(response)
        assert response.status_code == 405


class SimulatorCase(TrielTestCase):

    def test_list_simulators(self):
        response = requests.get(SIMULATOR_URL)
        self.print_response(response)
        assert response.status_code == 200

    def test_get_simulators(self):
        response = requests.get(SIMULATOR_URL + '1/')
        self.print_response(response)
        assert response.status_code == 200

    def test_post_simulators(self):
        response = requests.post(SIMULATOR_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 405

    def test_patch_simulators_name(self):
        response_wo_changes = requests.get(SIMULATOR_URL + '1/')
        response = requests.patch(SIMULATOR_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 200
        assert response.json() == response_wo_changes.json()

    def test_patch_simulators_path(self):
        response = requests.patch(SIMULATOR_URL + '1/', json={"path": ""})
        self.print_response(response)
        assert response.status_code == 400

    def test_delete_simulators(self):
        response = requests.delete(SIMULATOR_URL + '1/')
        self.print_response(response)
        assert response.status_code == 405


class SuitesCase(TrielTestCase):

    def test_list_suites(self):
        response = requests.get(SUITE_URL)
        self.print_response(response)
        assert response.status_code == 200

    def test_get_suites(self):
        response = requests.get(SUITE_URL + '1/')
        self.print_response(response)
        assert response.status_code == 200

    def test_post_suites(self):
        response = requests.post(SUITE_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 405

    def test_patch_suites(self):
        response = requests.patch(SUITE_URL + '1/', json={"name": "new_name"})
        self.print_response(response)
        assert response.status_code == 405

    def test_delete_suites(self):
        response = requests.delete(SUITE_URL + '1/')
        self.print_response(response)
        assert response.status_code == 405


if __name__ == '__main__':
    unittest.main()
