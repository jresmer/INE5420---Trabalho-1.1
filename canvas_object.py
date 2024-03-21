from abc import ABC, abstractmethod
from color import Color


# TODO - rever necessidade de tkinte_id ser passado por parâmetro
class CanvasObject(ABC):

    def __init__(self, coord: tuple, color: Color, name: str,
                    tkinter_id: int, canvas) -> None:
        
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas

    @abstractmethod
    def draw(self, viewport: tuple, window: tuple) -> None:

        pass
