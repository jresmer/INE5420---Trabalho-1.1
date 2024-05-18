from canvas_object import CanvasObject
from utils import Clipping, Utils
import numpy as np


class BezierSurface(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:

        coord = []
        for i in range(24):
            if i % 4 == 0 and i > 0:
                line = [(0,0,(i-1)*10),(100,100,(i-1)*10),(100,500,(i-1)*10),(400,300,(i-1)*10)]
            else: 
                line = [(0,0,i*10),(100,100,i*10),(100,500,i*10),(400,300,i*10)]
            print(line)
            coord += line
        
        for point in coord:
            if len(point) != 3:
                print(point)
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
        
        #calculating viewport coordinates
        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        for i in range(len(window_coords)):
            
            x, y = window_coords[i]

            x = vp_xmin + (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            window_coords[i] = (x, y)

        tk_ids = []
        for i in range(len(window_coords)//16):

            retalho = window_coords[i*16:(i+1)*16]

            # define geometry matrix
            Gx = []
            Gy = []
            for i in range(4):
                Gx.append([None,None,None,None])
                Gy.append([None,None,None,None])
                for j in range(4):
                    Gx[i][j] = retalho[i*4+j][0]
                    Gy[i][j] = retalho[i*4+j][1]

            values = [0, 0.2, 0.4, 0.6, 0.8, 1] # TODO - melhorar
            

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
                intercept = Clipping.curve_clipping(viewport, retalho, Px, Py)
                aux(intercept, viewport, Px, Py, self.__n_vars, self.__range, tk_ids)

            for s in values:

                S = [np.power(s, 3), np.power(s, 2), s, 1]
                
                Px = np.matmul(S, MGxMt)
                Py = np.matmul(S, MGyMt)

                # TODO - revisar se faz sentido
                intercept = Clipping.curve_clipping(viewport, retalho, Px, Py)
                aux(intercept, viewport, Px, Py, self.__n_vars, self.__range, tk_ids)

        self.set_tkinter_id(tk_ids)

    def delete(self):
        
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)
