from canvas_object import CanvasObject
from color import Color


class Line(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: Color, name: str, tkinter_id: int, canvas) -> None:
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas

    def get_name(self):
        return self.__name

    def draw(self, viewport: tuple, window: tuple, zoom: float) -> None:
        
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = window
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        (x0, y0), (x1, y1) = self.__coord

        x0_vp = (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y0_vp = (y0 - window_ymin) * (vp_ymax - vp_ymin) / (window_ymax - window_ymin)
        x1_vp = (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y1_vp = (y1 - window_ymin) * (vp_ymax - vp_ymin) / (window_ymax - window_ymin)

        self.__tkinter_id = self.__canvas.create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.__color, width=zoom)

    def delete(self):
        self.__canvas.delete(self.__tkinter_id)

