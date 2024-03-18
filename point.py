from canvas_object import CanvasObject


class Point(CanvasObject):

    def draw(self, viewport: tuple, window: tuple) -> None:

        window_xmin, window_ymin, window_xmax, window_ymax = window
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        x, y = self.__coord

        x_vp = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y_vp = (y - window_ymin) * (vp_ymax - vp_ymin) / (window_ymax - window_ymin)

        self.__canvas.create_oval(x_vp - 1, y_vp - 1, x_vp + 1, y_vp + 1, fill=self.__color)
