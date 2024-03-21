from canvas_object import CanvasObject
from color import Color


class Point(CanvasObject):
    def __init__(self, coord: tuple, color: Color, name: str, tkinter_id: int, canvas) -> None:
        self.__coord = coord
        self.__color = color
        self.__name = name
        self.__tkinter_id = tkinter_id
        self.__canvas = canvas

    def draw(self, viewport: tuple, window: tuple) -> None:
        
        self.__canvas.delete(self.__tkinter_id)

        window_xmin, window_ymin, window_xmax, window_ymax = window
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        x, y = self.__coord

        x_vp = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y_vp = (y - window_ymin) * (vp_ymax - vp_ymin) / (window_ymax - window_ymin)

        self.__tkinter_id = self.__canvas.create_oval(x_vp - 1, y_vp - 1, x_vp + 1, y_vp + 1, fill=self.__color)
