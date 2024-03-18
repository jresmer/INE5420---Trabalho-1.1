from abc import ABC, abstractmethod


class WindowGUI(ABC, ):

    def __init__(self, controller):
        
        self.__controller = controller

    @abstractmethod
    def init_window(self,world) -> None:

        pass
    
    @abstractmethod
    def init_widgets(self, world) -> None:

        pass