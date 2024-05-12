from canvas_object import CanvasObject
from utils import Clipping


class Line(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        new_coords = []
        for point in coord:
            if len(point) != 2:
                self.set_invalid()
                return
            new_coords.append(point+(0,))

        super().__init__(new_coords, color, name, tkinter_id, canvas)

        if len(coord) > 2:
            self.set_invalid()

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport


        new_coords = Clipping.instance().line_clipping([-1,-1,1,1],window_coords)

        if new_coords == None:
            return
        
        (x0,y0),(x1,y1) = new_coords

        x0_vp = vp_xmin + (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y0_vp = vp_ymin + (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
        x1_vp = vp_xmin + (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y1_vp = vp_ymin + (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

        new_tkinter_id = self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom)
        self.set_tkinter_id(new_tkinter_id)

    def delete(self):
        self.get_canvas().delete(self.get_tkinter_id())
