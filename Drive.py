import time
import logging
from threading import Thread
from DrivePainter import DrivePainter
from Gui import Gui
from QueuePainter import QueuePainter
from StatusOfDrive import StatusOfDrive
from Loadbalancer import Loadbalancer
from StatusOfFile import StatusOfFile


class Drive(Thread):
    global_id = 0

    def __init__(self, loadbalancer: Loadbalancer, gui: Gui):
        super().__init__(name=f"Drive {Drive.global_id}")
        self.__status = StatusOfDrive.WAITING_FOR_CLIENT
        self.__client_to_serve = None
        self.__id = Drive.global_id
        self.__loadbalancer = loadbalancer
        Drive.global_id += 1
        self.__list_of_saved_files = []
        self.__run = True
        self.gui = gui

    def run(self):
        logging.info(f'Drive {self.__id} has run')
        while self.__run:
            if self.__status == StatusOfDrive.WAITING_FOR_CLIENT:
                self.__client_to_serve = self.__loadbalancer.serve_request_from_drive()
                if self.__client_to_serve is not None:
                    logging.info(f'Drive {self.__id} asked for a client. Got User {self.__client_to_serve.client_id}')
                    self.__status = StatusOfDrive.BUSY
                    self.__save_one_file_for_client()

    def __save_one_file_for_client(self):
        if self.__client_to_serve is not None:
            qp = QueuePainter(self.__client_to_serve.client_id, self.gui)
            saved_file = self.__client_to_serve.save_file()
            qp.actualize_client_files(self.__client_to_serve)
            if saved_file is not None:
                dp = DrivePainter(self.__id, self.gui)
                logging.info(f'Saving a {saved_file.size}kb file of client {self.__client_to_serve.client_id} in progress')
                self.__status = StatusOfDrive.BUSY
                while saved_file.remaining_upload_time > 0:
                    time.sleep(1)
                    if saved_file.remaining_size_to_upload > 500:
                        saved_file.remaining_size_to_upload = saved_file.remaining_size_to_upload - 500
                        saved_file.remaining_upload_time = saved_file.remaining_upload_time - (1. / 60)
                    else:
                        saved_file.remaining_size_to_upload = 0
                        saved_file.remaining_upload_time = 0
                        self.__list_of_saved_files.append(saved_file)
                        self.__status = StatusOfDrive.WAITING_FOR_CLIENT
                    dp.draw_uploading_progress((saved_file.initial_size-saved_file.remaining_size_to_upload)/saved_file.initial_size, self.__client_to_serve, saved_file)
                self.__list_of_saved_files.append(saved_file)
                logging.info(f'File {self.__list_of_saved_files[-1].id} saved for client {self.__client_to_serve.client_id}')
                self.__client_to_serve = None
                saved_file.status = StatusOfFile.UPLOADED
                time.sleep(0.1)
                dp.init_drawing()

