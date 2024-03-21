from point import Point
from line import Line
from color import Color
from polygon import Polygon

class World:
    def __init__(self) -> None:
        self.__object_list = []
        self.__viewport = [0,0,500,500]
        self.__window = [0,0,500,500]

    def create_point(self, coord: tuple, canvas):
        point = Point(coord, Color.RED, "Ponto1", "", canvas)
        self.__object_list.append(point)
        point.draw(self.__viewport, self.__window)

    def create_line(self, coord: tuple, canvas):
        line = Line(coord, Color.BLUE, "Linha1", "", canvas)
        self.__object_list.append(line)
        line.draw(self.__viewport, self.__window)

    def create_polygon(self, coord: tuple, canvas):
        polygon = Polygon(coord, Color.BLUE, "Poligono1", "", canvas)
        self.__object_list.append(polygon)
        polygon.draw(self.__viewport, self.__window)
    
    def move_window(self, dx, dy):

        self.__window[0] += dx
        self.__window[1] += dy
        self.__window[2] += dx
        self.__window[3] += dy
 
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window)