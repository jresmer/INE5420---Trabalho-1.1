from canvas_object import CanvasObject
from utils import Clipping, Utils
import tkinter as tk
import sympy as sp

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

            x = vp_xmin +(x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            window_coords[i] = (x, y)
   
        #Verificando casca
        p1, p2, p3, p4 = window_coords

        min_y = vp_ymax+1
        max_y = -1
        min_x = vp_xmax + 1
        max_x = -1
        for (x,y) in [p1,p2,p3,p4]:
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x 

            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y  
        
        coords_casca = [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x,min_y)]

        casca_inside = []
        for (x,y) in coords_casca:
            casca_inside.append(Clipping.point_clipping(viewport, (x,y)))
        
        # if not any(casca_inside):
        #     print(casca_inside)
        #     return
        
        # calculating points between p1 and p4
        # TODO - determinar número de pontos a serem desenhados

        ax,bx,cx,dx = Utils.get_bezier_coeficients([p1[0], p2[0], p3[0], p4[0]])
        ay,by,cy,dy = Utils.get_bezier_coeficients([p1[1], p2[1], p3[1], p4[1]])

        #Teste para pontos de intersecção
        t = sp.Symbol('t', real = True)
        print("\n\n")
        print("T interceptando vp_xmin")
        for i in sp.solve(ax*t**3 + bx*t**2 + cx*t + dx - vp_xmin,t):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and y <= vp_ymax and y >= vp_ymin:
                print(x,y)
                print(i)
        print()
        print("T interceptando vp_xmax")
        for i in sp.solve(ax*t**3 + bx*t**2 + cx*t + dx - vp_xmax,t):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and y <= vp_ymax and y >= vp_ymin:
                print(x,y)
                print(i)
        print()

        print("T interceptando vp_ymin")
        result = sp.solve(ay*t**3 + by*t**2 + cy*t + dy - vp_ymin,t)
        print(result)
        for i in result:
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and x <= vp_xmax and x >= vp_xmin:
                print(x,y)
                print(i)
        
        print()

        print("T interceptando vp_ymax")
        result = sp.solve(ay*t**3 + by*t**2 + cy*t + dy - vp_ymax,t)
        print(result)
        for i in result:
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and x <= vp_xmax and x >= vp_xmin:
                print(x,y)
                print(i)
        print()

        coords = []

        t_to_be_calculated = [i*0.04 for i in range(25)]

        for t in t_to_be_calculated:

            t_square = t*t
            t_cubic = t_square*t
            x = ax*t_cubic + bx*t_square + cx*t + dx
            y = ay*t_cubic + by*t_square + cy*t + dy

            coords.append((x,y))
        
        all_inside = all(casca_inside)

        # drawing curve
        tkinter_ids = []

        for i in range(0, len(coords) - 1):
            x0, y0 = coords[i]
            x1, y1 = coords[i+1]

            if all_inside or Clipping.point_clipping(viewport, (x0,y0)):
                tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill=self.get_color())
                tkinter_ids.append(tk_id)

        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)