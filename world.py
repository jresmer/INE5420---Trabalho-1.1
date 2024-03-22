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
