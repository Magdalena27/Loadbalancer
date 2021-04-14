from StatusOfFile import StatusOfFile


class File:
    global_id = 0

    def __init__(self, size):
        self.__id = File.global_id
        File.global_id += 1
        self.__initial_size = size
        self.__size = size
        self.__remaining_size_to_upload = size
        self.__total_time_of_uploading = size / (500 * 60)
        self.__remaining_time_to_uploads_end = self.__total_time_of_uploading
        self.__status = StatusOfFile.TO_UPLOAD

    @property
    def total_time_of_uploading(self):
        return self.__total_time_of_uploading

    @property
    def remaining_size_to_upload(self):
        return self.__remaining_size_to_upload

    @remaining_size_to_upload.setter
    def remaining_size_to_upload(self, value):
        self.__remaining_size_to_upload = value

    @property
    def remaining_upload_time(self):
        return self.__remaining_time_to_uploads_end

    @remaining_upload_time.setter
    def remaining_upload_time(self, value):
        self.__remaining_time_to_uploads_end = value

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def __lt__(self, other):
        return self.__size < other.size

    @property
    def size(self):
        return self.__size

    @property
    def initial_size(self):
        return self.__initial_size

