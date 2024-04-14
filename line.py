from canvas_object import CanvasObject
from utils import Clippling


class Line(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        self.delete()
    
        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        new_coords = Clippling.liang_barsky([-1,-1,1,1],window_coords)
        if new_coords == None:
            return
        
        (x0,y0),(x1,y1) = new_coords

        x0_vp = (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y0_vp = (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
        x1_vp = (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y1_vp = (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

        new_tkinter_id = self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom)
        self.set_tkinter_id(new_tkinter_id)

    def delete(self):
        self.get_canvas().delete(self.get_tkinter_id())

