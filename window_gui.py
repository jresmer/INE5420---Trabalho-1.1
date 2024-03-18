from abc import ABC


class WindowGUI(ABC, ):
    def __init__(self, controller):
        self.__controller = controller

    def init_window(self,world) -> None:

        pass
        
    def init_widgets(self, world) -> None:

        pass