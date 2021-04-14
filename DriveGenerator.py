from Drive import Drive
from DrivePainter import DrivePainter
from Loadbalancer import Loadbalancer


class DriveGenerator:
    def __init__(self, gui):
        self.gui = gui
        self.__list_of_drivers = []

    def generate_drivers(self, number_of_drivers: int, loadbalancer: Loadbalancer):
        for driver in range(number_of_drivers):
            drive = Drive(loadbalancer, self.gui)
            dp = DrivePainter(driver, self.gui)
            dp.init_drawing()
            self.__list_of_drivers.append(drive)

    def run_drivers(self):
        if len(self.__list_of_drivers) > 0:
            for driver in self.__list_of_drivers:
                driver.start()
        else:
            print('There is no drive to run!')

