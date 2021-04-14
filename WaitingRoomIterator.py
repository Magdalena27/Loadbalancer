class WaitingRoomIterator:
    def __init__(self, waiting_room):
        self._waiting_room = waiting_room
        self._index = 0

    def __next__(self):
        if self._index < len(self._waiting_room.__queue):
            result = self._waiting_room.__queue[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration
