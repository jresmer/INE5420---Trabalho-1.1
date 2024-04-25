from canvas_object import CanvasObject
from utils import Clipping, Utils
import numpy as np

class BSplineCurve(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:
        super().__init__(coord, color, name, tkinter_id, canvas)
        # length of coord list is not multiple of 4
        if len(coord) < 4:
            self.set_invalid()


    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:
        
        # delete all previously drawn lines
        self.delete()

        #calculating viewport coordinates
        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        for i in range(len(window_coords)):
             
            x, y = window_coords[i]

            x = vp_xmin + (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            window_coords[i] = (x, y)
   
        tkinter_ids = []

            #Clippings
        for i in range(4,len(window_coords)+1):
            p1,p2,p3,p4 = window_coords[i-4:i+1]

            ax,bx,cx,dx = Utils.get_bspline_coeficients([p1[0], p2[0], p3[0], p4[0]])
            ay,by,cy,dy = Utils.get_bspline_coeficients([p1[1], p2[1], p3[1], p4[1]])

            # t_intercept = Clipping.curve_clipping(viewport, [p1,p2,p3,p4], [ax,bx,cx,dx], [ay,by,cy,dy])
            
            #Calculating number of ts
            vx, vy = (vp_xmax-vp_xmin, vp_ymax-vp_ymin)
            dist_vp = np.sqrt(vx ** 2 + vy ** 2)

            vx, vy = (p4[0]-p1[0], p4[1]-p1[1])
            dist_curve = np.sqrt(vx ** 2 + vy ** 2)

            razao = dist_curve/dist_vp

            # if razao > 1:
            #     number_of_ts = 1000
            # elif razao < 0.1:
            #     number_of_ts = 100
            # else:
            #     number_of_ts = int(1000*razao)
            number_of_ts = 500

            range_t = 1/number_of_ts

            range_t_sqr = range_t*range_t
            range_t_cub = range_t_sqr*range_t

            x0 = dx
            delta_x = ax*range_t_cub + bx*range_t_sqr + cx*range_t
            delta2_x = 6*ax*range_t_cub + 2*bx*range_t_sqr
            delta3_x = 6*ax*range_t_cub

            y0 = dy
            delta_y = ay*range_t_cub + by*range_t_sqr+ cy*range_t
            delta2_y = 6*ay*range_t_cub + 6*ay*range_t_sqr*y0 + 2*by*range_t_sqr
            delta3_y = 6*ay*range_t_cub

            for i in range(number_of_ts):

                x1 = x0 + delta_x
                delta_x = delta_x + delta2_x
                delta2_x = delta2_x + delta3_x

                y1 = y0 + delta_y
                delta_y = delta_y + delta2_y
                delta2_y = delta2_y + delta3_y

                tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill=self.get_color())
                tkinter_ids.append(tk_id)
            
                x0, y0 = x1,y1
            

            #Checking if start drawing
            # draw = False
            # if vp_xmin <= p1[0] and p1[0] <= vp_xmax and vp_ymin <= p1[1] and p1[1] <= vp_ymax:
            #     draw = True

            #Calculate t for each segment
            # coords = []

            # for i in range(len(t_intercept)-1):
                
            #     if draw:
            #         segment_coords = []
            #         lim_if = int(t_intercept[i]*number_of_ts) + 1
            #         lim_sup = int(t_intercept[i+1]*number_of_ts) - 1
            #         t_to_be_calculated = [t_intercept[i]] + [x*range_t for x in range(lim_if, lim_sup+1)] + [t_intercept[i+1]]

            #         for t in t_to_be_calculated:

            #             t_square = t*t
            #             t_cubic = t_square*t
            #             x = ax*t_cubic + bx*t_square + cx*t + dx
            #             y = ay*t_cubic + by*t_square + cy*t + dy

            #             segment_coords.append((x,y))
            #         coords.append(segment_coords)
            #     draw = not draw

            # drawing curve
            

            # for segment in coords:
            #     for i in range(0, len(segment) - 1):
            #         x0, y0 = segment[i]
            #         x1, y1 = segment[i+1]

            #         tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill=self.get_color())
            #         tkinter_ids.append(tk_id)

        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)