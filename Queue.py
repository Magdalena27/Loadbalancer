from threading import Lock
from Client import Client
from WaitingRoom import WaitingRoom


class Queue:
    def __init__(self):
        self.__queue = []
        self.lock = Lock()

    def __getitem__(self, item):
        return self.__queue[item]

    @property
    def queue(self):
        self.lock.acquire()
        queue = self.__queue
        self.lock.release()
        return queue

    def add_to_queue(self, client: Client):
        self.lock.acquire()
        self.__queue.append(client)
        self.lock.release()

    def add_group_of_clients(self, waiting_room: WaitingRoom):
        self.lock.acquire()
        self.__queue.extend(waiting_room)
        self.lock.release()

    def sort(self):
        self.lock.acquire()
        self.__queue.sort(reverse=True)
        self.lock.release()

    def count_length(self):
        self.lock.acquire()
        queue_length = len(self.__queue)
        self.lock.release()
        return queue_length

    def remove(self, client):
        self.__queue.remove(client)
