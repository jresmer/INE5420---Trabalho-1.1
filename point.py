from canvas_object import CanvasObject
from utils import Clipping

class Point(CanvasObject):
    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        if len(coord) > 3: #len([x,y,z]) > 2
            self.set_invalid()
        elif len(coord) == 2:
            new_coord = [(coord[0], coord[1], 0)]
            super().__init__(new_coord, color, name, tkinter_id, canvas)
        else:
            new_coord = [(coord[0], coord[1], coord[2])]
            super().__init__(new_coord, color, name, tkinter_id, canvas)


    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport

        [(x, y)] = window_coords

        if not Clipping.point_clipping([-1,-1,1,1], (x,y)):
            return 
        
        x_vp = vp_xmin + (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y_vp = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
  
        diff = int(1 * zoom)

        new_tkinter_id = self.get_canvas().create_oval(x_vp - diff, y_vp - diff, x_vp + diff, y_vp + diff, fill=self.get_color())
        self.set_tkinter_id(new_tkinter_id)

    def delete(self):
        self.get_canvas().delete(self.get_tkinter_id())
