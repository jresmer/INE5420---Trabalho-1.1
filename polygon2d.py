from canvas_object import CanvasObject
from utils import Clipping, Utils
from test import suthHodgClip

class Polygon2D(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        
        for point in coord:
            if len(point) != 3:
                self.set_invalid()
                return

        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport

        # new_window_coords = Utils.toClockwise(window_coords)

        new_window_coords = suthHodgClip(window_coords,[(-1,-1),(-1,1),(1,1),(1,-1)])

        coords_vp = []
        tkinter_ids = []

        if new_window_coords == []:
            return

        for (x,y) in new_window_coords:

            x_vp = vp_xmin + (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y_vp = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

            coords_vp.append(x_vp)
            coords_vp.append(y_vp)

        tkinter_ids.append(self.get_canvas().create_polygon(*coords_vp, fill=self.get_color(), width=zoom))
        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for id in self.get_tkinter_id():
            self.get_canvas().delete(id)
