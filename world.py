from point import Point
from color import Color

class World:
    def __init__(self) -> None:
        self.__object_list = []
        self.__viewport = [0,0,500,500]
        self.__window = [0,0,500,500]

    def create_point(self, coord: tuple, canvas):
        point = Point(coord, Color.RED, "Ponto1", "", canvas)
        self.__object_list.append(point)
        point.draw(self.__viewport, self.__window)
    
    def move_window(self, dx, dy):

        self.__window[0] += dx
        self.__window[1] += dy
        self.__window[2] += dx
        self.__window[3] += dy
 
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window)