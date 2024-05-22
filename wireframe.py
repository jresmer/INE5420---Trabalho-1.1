from canvas_object import CanvasObject
from utils import Clipping


class Wireframe(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:

        for point in coord:
            if len(point) != 3:
                self.set_invalid()
                return

        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport

        new_window_coords = window_coords[:]
        tkinter_ids = []

        if new_window_coords == []:
            return

        x0, y0 = new_window_coords[0]

        for (x1,y1) in new_window_coords[1:]:
            new_coords = Clipping.cohen_sutherland([-1,-1,1,1],[(x0,y0),(x1,y1)])
            if new_coords != None:

                (x0_vp,y0_vp),(x1_vp,y1_vp) = new_coords
                x0_vp = vp_xmin + (x0_vp - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
                y0_vp = vp_ymin + (1 - (y0_vp - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
                x1_vp = vp_xmin + (x1_vp - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
                y1_vp = vp_ymin + (1 - (y1_vp - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

                tkinter_ids.append(self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom))

            x0, y0 = x1, y1
        
        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)
