from Gui import Gui


class DrivePainter:
    def __init__(self, drive_id, gui: Gui):
        self.drive_id = drive_id
        self.gui =gui
        self.x1 = 50
        self.x2 = 400 + self.x1
        self.y1 = drive_id * (110 + 10) + self.x1
        self.y2 = self.y1 + 110
        self.name = f'Drive {drive_id}'

    def init_drawing(self):
        self.gui.redraw_drives(lambda c: self.draw_drive(c))

    def draw_drive(self, c):
        c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='LightBlue1', tags=self.name)

    def draw_uploading_progress(self, percent_progress, client, file):
        self.gui.redraw_drives(lambda c: self.draw_drive(c))
        self.gui.redraw_drives(lambda c: self.draw_progress_bar(c, percent_progress))
        self.gui.redraw_drives(lambda c: c.create_text(self.x1 + 200, self.y1 + 55,
                                                       text=f'Client: {client.client_id}\nfile: {file.id}',
                                                       tags=self.name))

    def draw_progress_bar(self, c, percent_progress):
        c.create_rectangle(self.x1, self.y1, percent_progress*self.x2, self.y2, fill='coral2')

