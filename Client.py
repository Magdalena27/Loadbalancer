import logging
from random import randint
from StatusOfClient import StatusOfClient
import ClientParams
import FileParams
from File import File


def draw_a_number_of_files():
    min_amount_of_files = ClientParams.min_amount_of_files
    max_amount_of_files = ClientParams.max_amount_of_files
    number_of_files = randint(min_amount_of_files, max_amount_of_files)
    return number_of_files


def draw_size_of_file():
    min_size_of_file_in_pow_of_two = FileParams.min_size_of_file_in_pow_of_two
    max_size_of_file_in_pow_of_two = FileParams.max_size_of_file_in_pow_of_two
    size_of_file_in_pow_of_two = randint(min_size_of_file_in_pow_of_two, max_size_of_file_in_pow_of_two)
    return pow(2, size_of_file_in_pow_of_two)


class Client:
    global_id = 0

    def __init__(self, number_of_files=0):
        self.__clientID = Client.global_id
        Client.global_id += 1
        self.__status = StatusOfClient.JUST_GENERATED
        self.__files_to_send = []
        self.__number_of_uploaded_files = 0
        self.__number_of_files_to_upload = 0
        self.__time_to_uploads_end_in_minutes = 0
        self.number_of_files = number_of_files
        self._init_client()
        self.__weight = 0

    def __lt__(self, other):
        return self.__weight < other.weight

    def _init_client(self):
        if self.number_of_files > 0:
            pass
        else:
            self.number_of_files = draw_a_number_of_files()
        self.__number_of_files_to_upload = self.number_of_files
        total_remaining_time = 0
        for file in range(self.number_of_files):
            size = draw_size_of_file()
            file = File(size)
            self.__files_to_send.append(file)
            file_uploading_time = file.total_time_of_uploading
            total_remaining_time += file_uploading_time
        self.__time_to_uploads_end_in_minutes = total_remaining_time
        self._sort_files()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def client_id(self):
        return self.__clientID

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value

    def save_file(self):
        self.__status = StatusOfClient.CONNECTING_WITH_DRIVE
        if self.__number_of_files_to_upload > 0:
            file_to_save = self.__files_to_send[0]
            self.__files_to_send.remove(file_to_save)
            self.__number_of_uploaded_files += 1
            self.__number_of_files_to_upload -= 1
            logging.info(f'Client {self.client_id} has still {self.__number_of_files_to_upload} files to upload.')
            self.__time_to_uploads_end_in_minutes -= file_to_save.total_time_of_uploading
            if self.__number_of_files_to_upload > 0:
                self.__status = StatusOfClient.IN_QUEUE
            else:
                self.__status = StatusOfClient.SERVED

            return file_to_save
        else:
            self.__status = StatusOfClient.SERVED
            return None

    def _sort_files(self):
        self.__files_to_send.sort(reverse=True)

    @property
    def number_of_uploaded_files(self):
        return self.__number_of_uploaded_files

    @property
    def number_of_files_to_upload(self):
        return self.__number_of_files_to_upload

    @property
    def time_to_uploads_end_in_minutes(self):
        return self.__time_to_uploads_end_in_minutes
