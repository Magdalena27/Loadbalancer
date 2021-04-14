import logging
from threading import Thread
from Client import Client
from Queue import Queue
from QueuePainter import QueuePainter
from StatusOfClient import StatusOfClient
from WaitingRoom import WaitingRoom
from WaitingRoomPainter import WaitingRoomPainter


class ButtonClientGenerator(Thread):
    def __init__(self, queue: Queue, waiting_room: WaitingRoom, gui):
        super().__init__(name="ClientGenerator")
        self.__queue = queue
        self.__waiting_room = waiting_room
        self.gui = gui

    def run(self) -> None:
        self.gui.set_add_specific_cli_btn_handler(handler=self.add_specific_client)
        self.gui.set_add_random_cli_btn_handler(handler=self.add_random_client)

    def generate_one_client(self):
        client = Client()
        return client

    def add_random_client(self):
        new_client = self.generate_one_client()
        if self.__queue.lock.locked():
            self.__waiting_room.add_to_queue(new_client)
            new_client.status = StatusOfClient.IN_WAITING_ROOM
            wrp = WaitingRoomPainter(new_client.client_id, self.gui)
            wrp.init_drawing(new_client)
            logging.info(f'User {new_client.client_id} added to waiting room')
        else:
            self.__queue.add_to_queue(new_client)
            new_client.status = StatusOfClient.IN_QUEUE
            qp = QueuePainter(new_client.client_id, self.gui)
            qp.init_drawing(new_client)
            logging.info(f'User {new_client.client_id} added to queue')

    def add_specific_client(self, number_of_files):
        new_client = self.generate_specific_client(number_of_files)
        if self.__queue.lock.locked():
            self.__waiting_room.add_to_queue(new_client)
            new_client.status = StatusOfClient.IN_WAITING_ROOM
            wrp = WaitingRoomPainter(new_client.client_id, self.gui)
            wrp.init_drawing(new_client)
            logging.info(f'User {new_client.client_id} added to waiting room')
        else:
            self.__queue.add_to_queue(new_client)
            new_client.status = StatusOfClient.IN_QUEUE
            qp = QueuePainter(new_client.client_id, self.gui)
            qp.init_drawing(new_client)
            logging.info(f'User {new_client.client_id} added to queue')

    def generate_specific_client(self, number_of_files):
        client = Client(number_of_files)
        return client
