from Client import Client
from WaitingRoomIterator import WaitingRoomIterator


class WaitingRoom:
    def __init__(self):
        self.__queue = []

    def __iter__(self):
        return WaitingRoomIterator(self)

    @property
    def queue(self):
        return self.__queue

    def add_to_queue(self, client: Client):
        self.__queue.append(client)

    def return_queue_length(self):
        return len(self.__queue)

    def count_length(self):
        queue_length = len(self.__queue)
        return queue_length
