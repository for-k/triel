import json
from enum import Enum
from typing import Dict

from triel.broker import Broker
from triel.entry import Tcp
from triel.topic import TrielTopic, ResponseConsumer


class Commands(Enum):
    GRAPH = "graph"
    SIMULATION = "simulate"
    CANCEL_SIMULATION = "cancel_simulation"


class TrielServer(Tcp, ResponseConsumer):
    SEPARATOR: str = ","
    REQ_COMMAND_TOPIC: Dict[str, TrielTopic] = {
        Commands.GRAPH.value: TrielTopic.GRAPH_REQ,
        Commands.SIMULATION.value: TrielTopic.SIMULATION_REQ,
        Commands.CANCEL_SIMULATION.value: TrielTopic.CANCEL_SIMULATION_REQ,
    }

    def parse_data(self, data: str):
        cmd, info_json = data.split(self.SEPARATOR, maxsplit=1)
        Broker.produce(self.REQ_COMMAND_TOPIC[cmd], json.loads(info_json))

    def on_graph_response(self, diagraph: str):
        self.write(f"{Commands.GRAPH.value}{self.SEPARATOR}{diagraph}")

    def on_simulation_started_response(self, tedam_json: Dict):
        pass

    def on_simulation_finished_response(self, tedam_json: Dict):
        pass

    def on_cancel_simulation_response(self, tedam_json: Dict):
        pass

    def on_stdout(self, sim_id: int, msg: str):
        pass
