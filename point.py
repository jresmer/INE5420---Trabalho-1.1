from canvas_object import CanvasObject
from color import Color


class Point(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: Color, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window: tuple, zoom: float) -> None:
        
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = window
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        x, y = self.get_coord()

        x_vp = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y_vp = (y - window_ymin) * (vp_ymax - vp_ymin) / (window_ymax - window_ymin)

        diff = int(1 * zoom)

        new_tkinter_id = self.get_canvas().create_oval(x_vp - diff, y_vp - diff, x_vp + diff, y_vp + diff, fill=self.get_color())
        self.set_tkinter_id(new_tkinter_id)

    def delete(self):
        self.get_canvas().delete(self.get_tkinter_id())
