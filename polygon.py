from canvas_object import CanvasObject
from color import Color
from line import Line


class Polygon(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: Color, name: str, tkinter_id: int, canvas) -> None:
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas
        self.__lines = []

    def get_name(self):
        return self.__name

    def draw(self, viewport: tuple, window: tuple) -> None:
        
        self.delete()

        x0, y0 = self.__coord[0]

        for (x1,y1) in self.__coord[1:]:
            line = Line(((x0,y0),(x1,y1)), self.__color, "LinhaPoligono1", "", self.__canvas)
            line.draw(viewport, window)
            self.__lines.append(line)

            x0, y0 = x1, y1

        x0, y0 = self.__coord[-1]
        x1, y1 = self.__coord[0]
        line = Line(((x0,y0),(x1,y1)), self.__color, "LinhaPoligono1", "", self.__canvas)
        line.draw(viewport, window)
        self.__lines.append(line)

    def delete(self):
        for line in self.__lines:
            line.delete()
        self.__lines = []