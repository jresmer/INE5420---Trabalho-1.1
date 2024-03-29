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

    
    def transform(self, m: np.array) -> list:

        new_coords = list()
        
        for coordinate in self.__coord:


            np_coord = np.array(coordinate + (1,))

            new_coord = np.matmul(np_coord, m)
            new_coord.tolist()
            x, y, z = new_coord
            new_coords.append((x,y))

        self.__coord = new_coords
    
    @abstractmethod
    def draw(self, viewport: tuple, window: tuple) -> None:
        pass

    @abstractmethod
    def delete(self):
        pass


    def get_name(self):
        return self.__name
    
    def get_coord(self):
        return self.__coord
    
    def get_color(self):
        return self.__color
    
    def get_tkinter_id(self):
        return self.__tkinter_id
    
    def set_tkinter_id(self, _tkinter_id):
        self.__tkinter_id = _tkinter_id
    
    def get_canvas(self):
        return self.__canvas
