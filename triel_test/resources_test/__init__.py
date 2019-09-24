import os


def resource_test_path(relative_path):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
