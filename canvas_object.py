from abc import ABC, abstractmethod
import numpy as np
from utils import Utils


# TODO - rever necessidade de tkinte_id ser passado por parâmetro
class CanvasObject(ABC):

    def __init__(self, coord: tuple, color: str, name: str,
                    tkinter_id: int, canvas) -> None:
        if len(coord) == 0:
            self.set_invalid()

        self.__obj_axis = (0,1,0)
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas
        self.__valid = True

    def get_obj_axis(self):
        return self.__obj_axis

    def att_obj_axis(self, m):
        self.__obj_axis = tuple(Utils.transform(self.__obj_axis, m))

    def transform(self, m: np.array) -> list:

        new_coords = list()
        
        for coordinate in self.__coord:

            coords = tuple(Utils.transform(coordinate, m))
            new_coords.append(coords)

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
    
    def get_center_coord(self):
        n = len(self.__coord)
        sum_x = 0
        sum_y = 0
        sum_z = 0
        for (x,y,z) in self.__coord:
            sum_x += x
            sum_y += y
            sum_y += z
        return (sum_x/n, sum_y/n, sum_z/n)
        
    @property    
    def valid(self):
        return self.__valid
    
    def set_invalid(self):
        self.__valid = False
