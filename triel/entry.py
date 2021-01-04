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
from _socket import SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR, timeout, socket
from threading import Event, Thread, current_thread
from time import sleep
from typing import List, Optional

JOIN_THREAD_STEP = 0.1


class Tcp:
    TCP_SOCKET_TIMEOUT = 1
    TCP_SOCKET_READ_BUFFER_SIZE = 4026
    TCP_MAX_CONNECTIONS = 5

    def __init__(self, port: int):
        self.clients: List[socket] = []  # Maintain a list of clients

        self.stop_reading: Event = Event()
        self.new_subs_stop: Event = Event()
        self.new_subs_thread: Thread = Thread(
            name="New tcp clients", target=self.allow_subs
        )

        # Start the tcp socket
        self.skt = socket(family=AF_INET, type=SOCK_STREAM)
        self.skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
        self.skt.settimeout(self.TCP_SOCKET_TIMEOUT)
        self.skt.bind(("", port))
        self.skt.listen(self.TCP_MAX_CONNECTIONS)
        self.new_subs_thread.start()

    def allow_subs(self) -> None:
        """thread routine to allow remote logging subscriptions"""
        while not self.new_subs_stop.is_set():
            try:
                client_socket, addr = self.skt.accept()
                client_socket.settimeout(self.skt.gettimeout())
                self.clients.append(client_socket)
                Thread(
                    name="Client Reader",
                    target=self.read_from_client,
                    args=[client_socket],
                ).start()
            except timeout:
                pass

    def read_from_client(self, client: socket) -> None:
        while not self.stop_reading.is_set():
            try:
                data = client.recv(
                    self.TCP_SOCKET_READ_BUFFER_SIZE
                )  # If we detach the client while reading It generates an OSError
                if data:
                    self.parse_data(data.decode())
                elif client.gettimeout() is not None:
                    sleep(
                        client.gettimeout()
                    )  # Avoid receiving empty data without timeout and overloading the cpu
            except (timeout, BlockingIOError):
                pass
            except Exception:
                break

    def write(self, frame: bytes) -> None:
        for client in self.clients:
            try:
                client.settimeout(None)
                client.sendall(frame)
                client.settimeout(self.skt.gettimeout())
            except Exception:
                pass

    def stop(self) -> None:
        # Close new clients thread
        if not self.new_subs_stop.is_set():
            self.new_subs_stop.set()
            join_thread(self.new_subs_thread)

        # Stop reading threads
        if not self.stop_reading.is_set():
            self.stop_reading.set()

        # Close client sockets
        for client in self.clients[:]:
            try:
                client.close()
            except Exception as err:
                logging.exception(err)

        # Close main socket
        self.skt.close()

    def parse_data(self, data: str):
        pass


def join_thread(thread: Thread, timeout_value: Optional[int] = None) -> None:
    """
    Non blocking joining thread operation
    """
    if thread is not None and thread != current_thread():
        while thread.is_alive():
            thread.join(JOIN_THREAD_STEP)
            if timeout_value is not None:
                timeout_value -= JOIN_THREAD_STEP
                if timeout_value <= 0:
                    raise TimeoutError("Timeout reached")
