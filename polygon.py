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

        outside_points = []
        for (x,y) in window_coords:
            outside_points.append(not Clipping.point_clipping([-1,-1,1,1], (x,y)))
        
        if all(outside_points):
            return

        new_window_coords = Clipping.adapted_weiler_atherton([-1,-1,1,1], window_coords)
        coords_vp = []
        tkinter_ids = []

        if new_window_coords == []:
            new_window_coords = window_coords

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