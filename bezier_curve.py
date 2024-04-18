from canvas_object import CanvasObject
from utils import Clipping


class BezierCurve(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        # delete all priviously drawn lines
        self.delete()

        #calculating viewport coordinates
        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        for i in range((len(window_coords))):
             
             x, y = window_coords[i]
             x = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
             y = (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
             window_coords[i] = (x, y)

        # clipping the curve   
        new_window_coords = Clipping.line_clipping([-1, -1, 1, 1], coords)
        if len(new_window_coords) == 0:
            return

        # calculating points between p1 and p4
        # TODO - determinar número de pontos a serem desenhados
        coords = []
        p1, p2, p3, p4 = window_coords
        t_to_be_calculated = list()
        for t in t_to_be_calculated:

            p = [0, 0]
            for i in range(len(p)):

                p[i] = p1[i] * (-1*t**3 + 3*t**2 - 3*t + 1) + p2[i] * (3*t**3 - 6*t**2 + 3*t) \
                    + p3[i] * (-3*t**3 + 3*t**2) + p4[i] * (t**3)
                
            coords.append(p)
        
        # drawing curve
        tkinter_ids = []
        for i in range(0, len(coords) - 1):
            x0, y0 = coords[i]
            x1, y1 = coords[i+1]
            
            tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill="green")
            tkinter_ids.append(tk_id)

        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)