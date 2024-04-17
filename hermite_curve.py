from canvas_object import CanvasObject
from utils import Clipping


class HermiteCurve(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        p1, r1, p4, r4 = coord
        coord = (p1, p4)
        super().__init__(coord, color, name, tkinter_id, canvas)
        self.__tangents = (r1, r4)

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        # delete all priviously drawn lines
        self.delete()

        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport

        # calculating points between p1 and p4
        coords = []
        p1, p4 = window_coords
        r1, r4 = self.__tangents
        # TODO - determinar número de pontos a serem desenhados
        t_to_be_calculated = list()
        for t in t_to_be_calculated:

            p = [0, 0]
            for i in range(len(p)):

                p[i] = p1[i] * (2*t**3 - 3*t**2 + 1) + p4[i] * (-2*t**3 + 3*t**2) \
                    + r1[i] * (t**3 - 2*t**2 + t) + r4[i] * (t**3 - t**2)
                
            coords.append(p)

        # clipping the curve   
        new_window_coords = Clipping.line_clipping([-1, -1, 1, 1], coords)
        if len(new_window_coords) == 0:
            return
        
        tkinter_ids = []
        x0, y0 = new_window_coords[0]

        # drawing lines between calculates points
        for (x1,y1) in new_window_coords[1:]:
            if not ((x0 == x1 == 1) or (x0 == x1 == -1) or (y0 == y1 == 1) or (y0 == y1 == -1)):
                x0_vp = vp_xmin + (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
                y0_vp = vp_ymin + (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
                x1_vp = vp_xmin + (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
                y1_vp = vp_ymin + (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

                tkinter_ids.append(self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom))

            x0, y0 = x1, y1
        
        x0, y0 = new_window_coords[-1]
        x1, y1 = new_window_coords[0]
        if not ((x0 == x1 == 1) or (x0 == x1 == -1) or (y0 == y1 == 1) or (y0 == y1 == -1)):
            x0_vp = vp_xmin + (x0 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y0_vp = vp_ymin + (1 - (y0 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            x1_vp = vp_xmin + (x1 - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y1_vp = vp_ymin + (1 - (y1 - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)

            tkinter_ids.append(self.get_canvas().create_line(x0_vp, y0_vp, x1_vp, y1_vp, fill=self.get_color(), width=zoom))
        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)