"""

 Copyright 2021 Teros Technology

 Ismael Perez Rojo
 Carlos Alberto Ruiz Naranjo
 Alfredo Saez

 This file is part of Triel.

 Triel is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Triel is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Triel.  If not, see <https://www.gnu.org/licenses/>.

"""
from abc import abstractmethod
from enum import auto
from typing import Dict

from triel.broker import Consumer, Topic


class TrielTopic(Topic):
    """
    Triel Topics
    """

    GRAPH_REQ = auto()
    GRAPH_RES = auto()

    SIMULATION_REQ = auto()
    SIMULATION_STARTED_RES = auto()
    SIMULATION_FINISHED_RES = auto()

    SIMULATION_STDOUT = auto()

    CANCEL_SIMULATION_REQ = auto()
    CANCEL_SIMULATION_RES = auto()


class GraphConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.activate_consumer(TrielTopic.GRAPH_REQ, self.on_graph_requested)

    @abstractmethod
    def on_graph_requested(self, tedam_json: Dict):
        pass


class SimulationConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.activate_consumer(TrielTopic.SIMULATION_REQ, self.on_simulation_requested)
        self.activate_consumer(
            TrielTopic.CANCEL_SIMULATION_REQ, self.on_cancel_simulation
        )

    @abstractmethod
    def on_simulation_requested(self, tedam_json: Dict):
        pass

    @abstractmethod
    def on_cancel_simulation(self, sim_id: int):
        pass


class ResponseConsumer(Consumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activate_consumer(TrielTopic.GRAPH_RES, self.on_graph_response)
        self.activate_consumer(TrielTopic.SIMULATION_STARTED_RES, self.on_simulation_started_response)
        self.activate_consumer(TrielTopic.SIMULATION_FINISHED_RES, self.on_simulation_finished_response)
        self.activate_consumer(
            TrielTopic.CANCEL_SIMULATION_RES, self.on_cancel_simulation_response
        )
        self.activate_consumer(
            TrielTopic.SIMULATION_STDOUT, lambda args: self.on_stdout(*args)
        )

    @abstractmethod
    def on_graph_response(self, tedam_json: Dict):
        pass

    @abstractmethod
    def on_simulation_started_response(self, tedam_json: Dict):
        pass

    @abstractmethod
    def on_simulation_finished_response(self, tedam_json: Dict):
        pass

    @abstractmethod
    def on_cancel_simulation_response(self, tedam_json: Dict):
        pass

    @abstractmethod
    def on_stdout(self, sim_id: int, msg: str):
        pass
