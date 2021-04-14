from tkinter import Tk, Canvas, BOTH, Frame, Label, GROOVE, LEFT, TOP, NW, FLAT, Button, CENTER, Spinbox
import ClientParams


class Gui:
    def __init__(self):
        self.window = self._create_window()
        self.waiting_room = self._create_waiting_room_visualisation()
        self.waiting_room_canvas = self._create_waiting_room_canvas()
        self.queue = self._create_queue()
        self.queue_canvas = self._create_queue_canvas()
        self.drives = self._create_place_for_drives()
        self.drives_canvas = self._create_canvas_for_drives()
        self.buttons = self._create_place_for_buttons()
        self.random_client_button = self._create_add_random_client_button()
        self.specific_client_button = self._create_add_specific_client_button()
        self.files_number_spinbox = self._create_files_number_spinbox()

    def _create_window(self):
        tk = Tk()
        tk.geometry("1400x700")
        tk.title("Loadbalancer simulation")
        return tk

    def _create_waiting_room_visualisation(self):
        waiting_room_frame = Frame(master=self.window, relief=GROOVE, borderwidth=5, background='gray25')
        waiting_room_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=NW)
        label = Label(master=waiting_room_frame, text='Waiting Room', foreground='ghost white', background='gray25')
        label.pack(side=TOP)
        return waiting_room_frame

    def _create_queue(self):
        queue_frame = Frame(master=self.window, relief=GROOVE, borderwidth=5, background='gray25')
        queue_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=NW)
        label = Label(master=queue_frame, text='Queue', foreground='ghost white', background='gray25')
        label.pack(side=TOP)
        return queue_frame

    def mainloop(self):
        self.window.mainloop()

    def _create_place_for_drives(self):
        drives_frame = Frame(master=self.window, relief=GROOVE, borderwidth=5, background='gray25')
        drives_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=NW)
        label = Label(master=drives_frame, text='Drives', foreground='ghost white', background='gray25')
        label.pack(side=TOP)
        return drives_frame

    def _create_place_for_buttons(self):
        buttons_frame = Frame(master=self.window, relief=FLAT, borderwidth=5, background='gray25')
        buttons_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=NW)
        return buttons_frame

    def _create_add_random_client_button(self):
        button = Button(master=self.buttons, text='Add random client')
        button.pack(anchor=CENTER)
        return button

    def _create_files_number_spinbox(self):
        label = Label(master=self.buttons, text='x:', foreground='ghost white', background='gray25')
        label.pack()
        spinbox = Spinbox(master=self.buttons, fg="blue", font=12, from_=ClientParams.min_amount_of_files, to=ClientParams.max_amount_of_files)
        spinbox.pack()
        return spinbox

    def _create_add_specific_client_button(self):
        button = Button(master=self.buttons, text='Add client with x files')
        button.pack(anchor=CENTER)
        return button

    def redraw_queue(self, fun, *args):
        self.queue_canvas.after(0, lambda: fun(self.queue_canvas, *args))

    def redraw_waiting_room(self, fun, *args):
        self.waiting_room_canvas.after(0, lambda: fun(self.waiting_room_canvas, *args))

    def redraw_drives(self, fun, *args):
        self.drives_canvas.after(0, lambda: fun(self.drives_canvas, *args))

    def set_add_random_cli_btn_handler(self, handler):
        self.random_client_button.configure(command=handler)

    def set_add_specific_cli_btn_handler(self, handler):
        self.specific_client_button.configure(command=lambda: handler(int(self.files_number_spinbox.get())))

    def _create_canvas_for_drives(self):
        canvas = Canvas(master=self.drives, background='gray25', border=0)
        canvas.pack(fill=BOTH, expand=1)
        return canvas

    def _create_queue_canvas(self):
        canvas = Canvas(master=self.queue, background='gray25', border=0, width=100)
        canvas.pack(fill=BOTH, expand=1)
        return canvas

    def _create_waiting_room_canvas(self):
        canvas = Canvas(master=self.waiting_room, background='gray25', border=0, width=100)
        canvas.pack(fill=BOTH, expand=1)
        return canvas
