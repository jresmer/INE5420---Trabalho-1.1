from canvas_object import CanvasObject
from utils import Clipping, Utils
import tkinter as tk
import sympy as sp
import numpy as np

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
        

        #Clippings
        coords = Clipping.curve_clipping(viewport, window_coords)
        
        all_inside = all(casca_inside)

        # drawing curve
        tkinter_ids = []

        for segment in coords:
            for i in range(0, len(segment) - 1):
                x0, y0 = segment[i]
                x1, y1 = segment[i+1]

                #TODO: Avaliar necessidade dessa checagem, talvez já fazer isso dentro do curve_clipping?
                if i + 1 == len(segment) - 1 or i == 0:
                    new_coords = Clipping.liang_barsky(viewport, [(x0,y0), (x1,y1)])
                    if new_coords != None:
                        (x0,y0),(x1,y1) = new_coords

                tk_id = self.get_canvas().create_line(x0, y0, x1, y1, fill=self.get_color())
                tkinter_ids.append(tk_id)

        self.set_tkinter_id(tkinter_ids)

    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)