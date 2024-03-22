from point import Point
from line import Line
from color import Color
from polygon import Polygon

class World:
    def __init__(self) -> None:
        self.__object_list = []
        self.__viewport = [0,0,500,500]
        self.__window = [0,0,500,500]

    def create_object(self, coord: tuple, color: Color, name: str, obj_type, canvas) -> None:

        new_object = obj_type(coord, color, name, "", canvas)
        self.__object_list.append(new_object)
        new_object.draw(self.__viewport, self.__window)

    #TODO: verificar se o obj está sendo deletado corretamente do canvas
    #TODO: melhorar sistema de busca (talvez usando dict para object list?)
    def delete_object(self, name):
        for i in range(len(self.__object_list)):
            if name == self.__object_list[i].get_name():
                self.__object_list[i].delete()
                obj = self.__object_list.pop(i)
                del obj
                print(f"Deleted: {name}")
                return
    
    def move_window(self, dx, dy):

        self.__window[0] += dx
        self.__window[1] += dy
        self.__window[2] += dx
        self.__window[3] += dy
 
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window)

    def get_last_object_name(self):
        return self.__object_list[-1].get_name()
    
    def zoom_window(self, pct_x: float, pct_y: float):

        # recover window
        min_x, min_y, max_x, max_y = self.__window

        # calculate new window size
        # calculate new x values
        multiplier = 1 + (pct_x / 2)
        center_x = (min_x + max_x) // 2
        min_diff = int((center_x - min_x) * multiplier)
        new_min_x = center_x - min_diff
        max_diff = int((max_x - center_x) * multiplier)
        new_max_x = max_diff + center_x
 
        # calculate new y values
        multiplier = 1 + (pct_y / 2)
        center_y = (min_y + max_y) // 2
        min_diff = int((center_y - min_y) * multiplier)
        new_min_y = center_y - min_diff
        max_diff = int((max_y - center_y) * multiplier)
        new_max_y = max_diff + center_y

        # set new window size
        self.__window = [new_min_x, new_min_y, new_max_x, new_max_y]

        # redraw canvas objects
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window)
