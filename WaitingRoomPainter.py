from Gui import Gui


class WaitingRoomPainter:
    def __init__(self, client_id, gui: Gui):
        self.client_id = client_id
        self.gui = gui
        self.x1 = 21
        self.x2 = 200 + self.x1
        self.y1 = client_id * (26 + 10) + 10
        self.y2 = self.y1 + 26
        self.name = f'Client {client_id}'

    def init_drawing(self, client):
        self.gui.redraw_waiting_room(lambda c: self.draw_client(c))
        self.gui.redraw_waiting_room(lambda c: c.create_text(self.x1+105, self.y1+13,
                                                      text=f'Client: {self.client_id} ({client.number_of_files_to_upload})'))

    def draw_client(self, c):
        c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='wheat1', tags=self.name)
