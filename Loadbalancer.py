from threading import Lock
from Queue import Queue
from StatusOfClient import StatusOfClient
from WaitingRoom import WaitingRoom


class Loadbalancer:
    def __init__(self, queue: Queue, waiting_room: WaitingRoom):
        self.__queue = queue
        self.__waiting_room = waiting_room
        self.lock = Lock()

    def serve_request_from_drive(self):
        self.lock.acquire()
        if self.__waiting_room.return_queue_length() > 0:
            for client in self.__waiting_room:
                client.status = StatusOfClient.IN_QUEUE
            self.__queue.add_group_of_clients(self.__waiting_room)
        if self.__queue.count_length() > 0:
            for client in self.__queue:
                if client.status == StatusOfClient.SERVED:
                    self.__queue.remove(client)

            next_client = self.return_best_client()
            if next_client is not None:
                next_client.status = StatusOfClient.CONNECTING_WITH_DRIVE
        else:
            next_client = None
        self.lock.release()
        return next_client

    def count_weight(self):
        number_of_clients = self.__queue.count_length()
        for client in range(number_of_clients):
            if self.__queue[client].status != StatusOfClient.CONNECTING_WITH_DRIVE:
                factor1 = number_of_clients / (client+1)
                factor2 = (1 + self.__queue[client].number_of_uploaded_files)/(self.__queue[client].number_of_files_to_upload + self.__queue[client].number_of_uploaded_files)
                factor3 = 5 / self.__queue[client].time_to_uploads_end_in_minutes
                client_weight = factor1 * factor2 * factor3
                self.__queue[client].weight = client_weight

    def sort_queue(self):
        self.count_weight()
        self.__queue.sort()

    def return_best_client(self):
        self.sort_queue()
        if self.__queue.count_length() > 0:
            return self.__queue[0]
        else:
            return None
