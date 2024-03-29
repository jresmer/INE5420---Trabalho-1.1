from canvas_object import CanvasObject
from color import Color
from line import Line


class Polygon(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: Color, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)
        self.__lines = []

    def draw(self, viewport: tuple, window: tuple, zoom: float) -> None:
        
        self.delete()

        x0, y0 = self.get_coord()[0]

        for (x1,y1) in self.get_coord()[1:]:
            line = Line(((x0,y0),(x1,y1)), self.get_color(), "Linha", "", self.get_canvas())
            line.draw(viewport, window, zoom)
            self.__lines.append(line)

            x0, y0 = x1, y1

        x0, y0 = self.get_coord()[-1]
        x1, y1 = self.get_coord()[0]
        line = Line(((x0,y0),(x1,y1)), self.get_color(), "Linha", "", self.get_canvas())
        line.draw(viewport, window, zoom)
        self.__lines.append(line)

    def delete(self):
        for line in self.__lines:
            line.delete()
        self.__lines = []