import logging
from datetime import datetime, timedelta, date, time
import random
from threading import Thread
from time import sleep
from Client import Client
from Gui import Gui
from Queue import Queue
from QueuePainter import QueuePainter
from StatusOfClient import StatusOfClient
from StatusOfClientGenerator import StatusOfClientGenerator
from WaitingRoom import WaitingRoom
from WaitingRoomPainter import WaitingRoomPainter


class ClientGenerator(Thread):
    def __init__(self, queue: Queue, waiting_room: WaitingRoom, time_of_action: float, gui):
        super().__init__(name="ClientGenerator")
        self.__queue = queue
        self.__waiting_room = waiting_room
        self.time_of_action_in_seconds = time_of_action
        self.start_time = datetime.now().time()
        self.end_time = datetime.combine(date.today(), time(self.start_time.hour, self.start_time.minute, self.start_time.second)) + timedelta(seconds=self.time_of_action_in_seconds)
        self.__status = StatusOfClientGenerator.WORKING
        self.gui = gui

    def run(self) -> None:

        while datetime.now().time() < self.end_time.time():
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
                sleep(random.randint(0, 4))
        logging.info('Generator stopped')
        self.__status = StatusOfClientGenerator.STOPPED_WORKING

    def generate_one_client(self):
        client = Client()
        return client

    @property
    def status(self):
        return self.__status

