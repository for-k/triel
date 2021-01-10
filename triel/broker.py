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

import logging
from enum import Enum
from queue import Queue, Empty
from threading import Thread
from time import sleep
from typing import Callable, Dict, List, Any, Optional, NamedTuple


class Topic(Enum):
    """ Base class for Topics """

    pass


class QueueData(NamedTuple):
    """ Info in a queue """

    topic: Topic
    msg: Any


class Consumer:
    """ Consumer base class """

    CONSUMER_SLEEP = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.internal_queue: Queue[Optional[QueueData]] = Queue()
        self.consumer_methods: Dict[
            Topic, Callable
        ] = {}  # Dict of topic and function to receive data from that topic
        self.consume_thread: Optional[Thread] = None

    def activate_consumer(self, topic: Topic, method: Callable) -> None:
        self.consumer_methods[topic] = method
        Broker.register_consumer(self, topic)

    def consume(self, topic: Topic, msg: Any):
        self.internal_queue.put(QueueData(topic, msg))
        if self.consume_thread is None or not self.consume_thread.is_alive():
            self.consume_thread = Thread(name="Consumer", target=self._do_consume)
            self.consume_thread.start()

    def _do_consume(self):
        while True:
            try:
                queue_data = self.internal_queue.get(block=False)
                if queue_data is not None:
                    try:
                        self.consumer_methods[queue_data.topic](queue_data.msg)
                    except Exception as err:
                        logging.exception(err)
                else:
                    break
            except Empty:
                sleep(self.CONSUMER_SLEEP)

    def stop(self):
        self.internal_queue.put(None)
        while self.consume_thread is not None and self.consume_thread.is_alive():
            pass


class Broker:
    consumers: Dict[Topic, List[Consumer]] = {}

    @classmethod
    def register_consumer(cls, instance: Consumer, topic: Topic) -> None:
        cls.__create_topic(topic)
        if instance not in cls.consumers[topic]:
            cls.consumers[topic].append(instance)

    @classmethod
    def produce(cls, topic: Topic, msg: Any) -> None:
        cls.__create_topic(topic)
        for consumer in cls.consumers[topic]:
            consumer.consume(topic, msg)

    @classmethod
    def stop(cls):
        for consumer_list in cls.consumers.values():
            for consumer in consumer_list:
                consumer.stop()

    @classmethod
    def __create_topic(cls, topic: Topic) -> None:
        if topic not in cls.consumers.keys():
            cls.consumers[topic] = []
