from canvas_object import CanvasObject
from utils import Clipping, Utils
import numpy as np


class BezierSurface(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:

        for point in coord:
            if len(point) != 3:
                self.set_invalid()
                return
            
        super().__init__(coord, color, name, tkinter_id, canvas)   
        # TODO - calculating number of ts
        self.__n_vars = 100
        self.__range = 1/100

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        def aux(intercept, vp, Px, Py, n, r, tk_ids):
            ax, bx, cx, dx = Px
            ay, by, cy, dy = Py
            vp_xmin, vp_ymin, vp_xmax, vp_ymax = vp
            
            draw = False
            if vp_xmin <= Px[-1] and Px[-1] <= vp_xmax and \
                vp_ymin <= Py[-1] and Py[-1] <= vp_ymax:
                draw = True

            #Calculate t for each segment
            coords = []
            for i in range(len(intercept)-1):
                
                if draw:
                    segment_coords = []
                    lim_if = int(intercept[i]*n) + 1
                    lim_sup = int(intercept[i+1]*n) - 1
                    to_be_calculated = [intercept[i]] + [x*r for x in range(lim_if, lim_sup+1)] + [intercept[i+1]]

                    for t in to_be_calculated:

                        t_square = t*t
                        t_cubic = t_square*t
                        x = ax*t_cubic + bx*t_square + cx*t + dx
                        y = ay*t_cubic + by*t_square + cy*t + dy

                        segment_coords.append((x,y))
                    coords.append(segment_coords)
                draw = not draw

            # drawing curve
            for segment in coords:
                for i in range(0, len(segment) - 1):
                    x0, y0 = segment[i]
                    x1, y1 = segment[i+1]

                    tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill=self.get_color())
                    tk_ids.append(tk_id)
        
        # define geometry matrix
        Gx = []
        Gy = []
        for i in range(4):
            Gx.append([])
            Gy.append([])
            for j in range(4):
                Gx[i][j] = window_coords[i*4+j][0]
                Gy[i][j] = window_coords[i*4+j][1]

        values = [0, 0.2, 0.4, 0.6, 0.8, 1] # TODO - melhorar
        tk_ids = []

        # Q(s, t) = S . M . G . Mt . Tt
        MGx = Utils.get_bezier_coeficients(Gx)
        MGy = Utils.get_bezier_coeficients(Gy)
        MGxMt = np.matmul(MGx, Utils.get_m_bezier())
        MGyMt = np.matmul(MGy, Utils.get_m_bezier())

        for t in values:
            T = [np.power(t, 3), np.power(t, 2), t, 1]
            
            Px = np.matmul(MGxMt, T)
            Py = np.matmul(MGyMt, T)

            # TODO - revisar se faz sentido
            intercept = Clipping.curve_clipping(viewport, window_coords, Px, Py)
            aux(intercept, viewport, Px, Py, self.__n_vars, self.__range, tk_ids)

        for s in values:

            S = [np.power(s, 3), np.power(s, 2), s, 1]
            
            Px = np.matmul(S, MGxMt)
            Py = np.matmul(S, MGyMt)

            # TODO - revisar se faz sentido
            intercept = Clipping.curve_clipping(viewport, window_coords, Px, Py)
            aux(intercept, viewport, Px, Py, self.__n_vars, self.__range, tk_ids)

        self.set_tkinter_id(tk_ids)

    def delete(self):
        
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)
