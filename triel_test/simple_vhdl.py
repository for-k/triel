import json
import logging
import os
import unittest
from socket import SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR, socket
from unittest import TestCase

from triel.__main__ import DEFAULT_PORT, main


class TcpClient(socket):
    READ_SIZE = 1024

    def __init__(self, server_ip: str = "localhost", server_port: int = DEFAULT_PORT, codec: str = "utf-8"):
        self.codec: str = codec
        super().__init__(family=AF_INET, type=SOCK_STREAM)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
        self.settimeout(None)
        self.connect((server_ip, server_port))

    def sendall(self, data: str, *args, **kwargs) -> None:
        super(TcpClient, self).sendall(data.encode(self.codec), *args, **kwargs)

    def read(self) -> str:
        try:
            return self.recv(self.READ_SIZE).decode(self.codec)
        except OSError:
            return ""


class SimpleTest(TestCase):
    started: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def launch_triel(cls):
        if not cls.started:
            main()
            cls.started = True

    @staticmethod
    def clean_json_str(data: str) -> str:
        return data.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "")

    @staticmethod
    def get_project_tedam() -> str:
        with open(os.path.join(os.path.dirname(__file__), "simple_vhdl", "tedam.json")) as fd:
            content = fd.read()
            tedam = json.loads(content)
            tedam["work_directory"] = os.path.join(os.path.dirname(__file__), "simple_vhdl")
            return json.dumps(tedam)

    def test_graph(self):
        self.launch_triel()
        skt = TcpClient()
        try:
            skt.sendall(f"graph,{self.get_project_tedam()}")
            response = skt.read()
            assert self.clean_json_str(response) == self.clean_json_str(
                '''graph,digraph {node [color="#069302" fillcolor=lightgray fontname=helvetica shape=component splines=line style="filled,rounded"]
                "C:\\Users\\alfre\\code\\triel\\triel_test\\simple_vhdl\\half_adder.vhd" [label="half_adder.vhd"]
                "C:\\Users\\alfre\\code\\triel\\triel_test\\simple_vhdl\\half_adder_simple_tb.vhd" [label="half_adder_simple_tb.vhd"]
                "C:\\Users\\alfre\\code\\triel\\triel_test\\simple_vhdl\\half_adder_simple_tb.vhd" -> "C:\\Users\\alfre\\code\\triel\\triel_test\\simple_vhdl\\half_adder.vhd"
                }''')
        except Exception as err:
            logging.exception(err)
        finally:
            skt.close()

    def test_simulation(self):
        self.launch_triel()
        skt = TcpClient()
        try:
            skt.sendall(f"simulate,{self.get_project_tedam()}")
            response = skt.read()
        except Exception as err:
            logging.exception(err)
        finally:
            skt.close()


if __name__ == '__main__':
    unittest.main()
