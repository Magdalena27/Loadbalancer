import logging
from ButtonClientGenerator import ButtonClientGenerator
from ClientGenerator import ClientGenerator
from DriveGenerator import DriveGenerator
from Gui import Gui
from Loadbalancer import Loadbalancer
from Queue import Queue
from WaitingRoom import WaitingRoom

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(threadName)s | %(message)s')


main_queue = Queue()
waiting_room = WaitingRoom()
loadbalancer = Loadbalancer(main_queue, waiting_room)
gui = Gui()
client_generator = ClientGenerator(main_queue, waiting_room, 10, gui)
button_client_generator = ButtonClientGenerator(main_queue, waiting_room, gui)


client_generator.start()

dg = DriveGenerator(gui)
dg.generate_drivers(5, loadbalancer)
dg.run_drivers()
button_client_generator.start()
gui.mainloop()
