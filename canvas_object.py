from abc import ABC, abstractmethod
from color import Color
import numpy as np


# TODO - rever necessidade de tkinte_id ser passado por parâmetro
class CanvasObject(ABC):

    def __init__(self, coord: tuple, color: Color, name: str,
                    tkinter_id: int, canvas) -> None:
        
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas

    def get_name(self):
        return self.__name
    
    def transform(self, coordinates: list, m: np.array) -> list:

        new_coords = list()

        for coordinate in self.__coord:

            np_coord = np.array(coordinate)

            new_coord = np.matmul(np_coord, m)
            new_coords.append(new_coord)
        
        self.__coord = new_coords
    
    @abstractmethod
    def draw(self, viewport: tuple, window: tuple) -> None:
        pass

    @abstractmethod
    def delete(self):
        pass
