from canvas_object import CanvasObject
from utils import Clipping

class Wireframe(CanvasObject):
    #TODO: Passar os atributos para classe pai e requisitar o atributo
    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)
        self.__lines = []

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        # polygons = Clipping.weiler_atherton([-1,-1,1,1], window_coords)
        tkinter_ids = []
        
        x0, y0 = window_coords[0]
            
        for (x1,y1) in window_coords[1:]:
            # if not ((abs(x0) == abs(x1) == 1) or (abs(y0) == abs(y1) == 1)):
            x0_vp = vp_xmin + (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y0_vp = vp_ymin + (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            x1_vp = vp_xmin + (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y1_vp = vp_ymin + (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

            tkinter_ids.append(self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom))

            x0, y0 = x1, y1
        
        x0, y0 = window_coords[-1]
        x1, y1 = window_coords[0]
        # if not ((abs(x0) == abs(x1) == 1) or (abs(y0) == abs(y1) == 1)):
        x0_vp = vp_xmin + (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y0_vp = vp_ymin + (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
        x1_vp = vp_xmin + (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
        y1_vp = vp_ymin + (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

        tkinter_ids.append(self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom))
        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)