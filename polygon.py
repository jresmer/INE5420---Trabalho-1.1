from canvas_object import CanvasObject
from utils import Clipping

class Polygon(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        # window_coords = Clipping.weiler_atherton([-1,-1,1,1], window_coords)
        coords_vp = []

        for (x,y) in window_coords:

            x_vp = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y_vp = (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

            coords_vp.append(x_vp)
            coords_vp.append(y_vp)

        tkinter_id = self.get_canvas().create_polygon(*coords_vp, fill=self.get_color(), width=zoom)
        self.set_tkinter_id(tkinter_id)

    def delete(self):
        self.get_canvas().delete(self.get_tkinter_id())