from point import Point
from line import Line
from color import Color
from polygon import Polygon
from copy import deepcopy
from math import ceil, sqrt

class World:
    def __init__(self) -> None:
        self.__object_list = []
        self.__viewport = [0,0,500,500]
        self.__window = [0,0,500,500]
        self.__zoom = 1

    def search_object_by_name(self, name: str):
        for obj in self.__object_list:
            if name == obj.get_name():
                return obj
        return None 

    def create_object(self, coord: tuple, color: Color, name: str, obj_type, canvas) -> None:
        if self.search_object_by_name(name) != None:
            return 2
        
        new_object = obj_type(coord, color, name, "", canvas)
        self.__object_list.append(new_object)

        new_object.draw(self.__viewport, self.__window, self.__zoom)
        return 1


    #TODO: verificar se o obj está sendo deletado corretamente do canvas
    #TODO: melhorar sistema de busca (talvez usando dict para object list?)
    def delete_object(self, name):
        for i in range(len(self.__object_list)):
            if name == self.__object_list[i].get_name():
                self.__object_list[i].delete()
                obj = self.__object_list.pop(i)
                del obj
                return
    
    def move_window(self, dx, dy):

        self.__window[0] += dx
        self.__window[1] += dy
        self.__window[2] += dx
        self.__window[3] += dy
 
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window, self.__zoom)
    
    def zoom_window(self, pct):

        # recover window
        min_x, min_y, max_x, max_y = self.__window

        # calculate new window size
        multiplier = sqrt(1 / (1 + pct))

        # calculate new x values
        center_x = (min_x + max_x) // 2
        min_diff = int((center_x - min_x) * multiplier)
        new_min_x = center_x - min_diff
        max_diff = ceil((max_x - center_x) * multiplier)
        new_max_x = max_diff + center_x
 
        # calculate new y values
        center_y = (min_y + max_y) // 2
        min_diff = int((center_y - min_y) * multiplier)
        new_min_y = center_y - min_diff
        max_diff = ceil((max_y - center_y) * multiplier)
        new_max_y = max_diff + center_y

        if new_max_x <= new_min_x + 20 or new_max_y <= new_min_y + 20:

            new_max_x, new_min_x = center_x + 10, center_x -10
            new_max_y, new_min_y = center_y + 10, center_y - 10

        if new_max_x > self.__viewport[2] or new_min_x < self.__viewport[0] or \
                new_max_y > self.__viewport[3] or new_min_y < self.__viewport[1]:

            new_min_x, new_min_y, new_max_x, new_max_y = deepcopy(self.__viewport)

        # set new window size
        self.__window = [new_min_x, new_min_y, new_max_x, new_max_y]

        previeous_size = (max_x - min_x) * (max_y - min_y)
        new_size = (new_max_x - new_min_x) * (new_max_y - new_min_y)
        diff = 1 - previeous_size / new_size
        self.__zoom -= diff

        # redraw canvas objects
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window, self.__zoom)
