from canvas_object import CanvasObject
from utils import Utils, Clipping
from copy import deepcopy
import numpy as np


class BSplineSurface(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:

        matrix = []

        for i in range(len(coord)):
            line = coord[i]

            if all([(not point) for point in line]):
                continue

            matrix.append([])
            for point in line:
                if point:
                    matrix[-1].append(point)
                else:
                    break
        
        self.__n_rows = len(matrix)

        if self.__n_rows < 4:
            self.set_invalid()
            return

        new_coords = []
        new_coords += matrix[0]
        
        self.__n_cols = len(matrix[0])

        if self.__n_cols < 4:
            self.set_invalid()
            return

        for i in range(1,len(matrix)):
            line = matrix[i]
            if len(line) != self.__n_cols:
                self.set_invalid()
                return
            
            new_coords += matrix[i]

        for point in new_coords:
            if len(point) != 3:
                self.set_invalid()
                return
        
        super().__init__(new_coords, color, name, tkinter_id, canvas)   

        self.__steps = 10

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        def aux(viewport, n, DDx_row, DDy_row, ids):    

            x0, delta_x, delta_x2, delta_x3 = DDx_row
            y0, delta_y, delta_y2, delta_y3 = DDy_row

            for _ in range(n):
                x1 = x0 + delta_x
                delta_x = delta_x + delta_x2
                delta_x2 = delta_x2 + delta_x3

                y1 = y0 + delta_y
                delta_y = delta_y + delta_y2
                delta_y2 = delta_y2 + delta_y3

                new_coords = Clipping.liang_barsky(viewport, [(x0,y0),(x1,y1)])
                if new_coords:
                    tk_id = self.get_canvas().create_line(*new_coords, fill=self.get_color())
                    ids.append(tk_id)
            
                x0, y0 = x1,y1

        # initializing ids list
        tk_ids = list()
        # calculating viewport coordinates
        window_xmin, window_ymin, window_xmax, window_ymax = [-1,-1,1,1]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = viewport
        for i in range(len(window_coords)):
            
            x, y = window_coords[i]

            x = vp_xmin + (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
            y = vp_ymin + (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
            window_coords[i] = (x, y)

        #recreating matrix coords
        matrix = []
        for row in range(self.__n_rows):
            line = window_coords[row*self.__n_cols: row*self.__n_cols+self.__n_cols]
            matrix.append(line)

        #drawing each retalho
        for row in range(self.__n_rows-3):
            for col in range(self.__n_cols-3):
                line1 = matrix[row    ][col:col+4]
                line2 = matrix[row + 1][col:col+4]
                line3 = matrix[row + 2][col:col+4]
                line4 = matrix[row + 3][col:col+4]

                retalho = line1+line2+line3+line4
                # plotting a submatrix
                """
                1. Calculate coeficients Cx, Cy, Cz:
                Cx = M * Gx * Mt
                Cy = M * Gy * Mt
                Cz = M * Gz * Mt
                """
                # define geometry matrix
                Gx = []
                Gy = []
                for i in range(4):
                    Gx.append([None,None,None,None])
                    Gy.append([None,None,None,None])
                    for j in range(4):
                        Gx[i][j] = retalho[i*4+j][0]
                        Gy[i][j] = retalho[i*4+j][1]

                m = Utils.get_m_bspline()
                mt = np.transpose(m)
                Cx = np.matmul(np.matmul(m, Gx), mt)
                Cy = np.matmul(np.matmul(m, Gy), mt)

                """
                2. Calculate deltas for ni steps:
                δs = 1/(ns - 1)
                δt = 1/(nt - 1)
                """
                delta_s = 1 / (self.__steps - 1)
                delta_t = 1 / (self.__steps - 1)

                """
                3. Generate the Eδs, Eδt and transpose Eδt
                """
                delta_s2 = delta_s * delta_s
                delta_s3 = delta_s2 * delta_s
                Eds = [[0, 0, 0, 1],
                    [delta_s3, delta_s2, delta_s, 0],
                    [6*delta_s3, 2*delta_s2, 0, 0],
                    [6*delta_s3, 0, 0, 0]]
                delta_t2 = delta_t * delta_t
                delta_t3 = delta_t2 * delta_t
                # already transposed
                EdtT = [[0, delta_t3, 6*delta_t3, 6*delta_t3],
                    [0, delta_t2, 2*delta_t2, 0],
                    [0, delta_t, 0, 0],
                    [1, 0, 0, 0]]

                """
                4. Calculate starting conditions:
                DDx = Eds * Cx * EdtT
                DDy = Eds * Cy * EdtT
                """
                DDx = np.matmul(Eds, np.matmul(Cx, EdtT))
                DDy = np.matmul(Eds, np.matmul(Cy, EdtT))
                # starting conditions for the curves in s (6, 7)
                DDx_, DDy_ = deepcopy(np.transpose(DDx)), deepcopy(np.transpose(DDy))

                """
                5. Draw the curve family in t
                """
                for i in range(self.__steps+1):
                    aux(viewport, self.__steps, DDx[0], DDy[0], tk_ids)
                    for j in range(len(DDx)-1):
                        DDx[j] = np.array(DDx[j]) + np.array(DDx[j+1])
                        DDy[j] = np.array(DDy[j]) + np.array(DDy[j+1])
                
                """
                6. Draw the curve family in s
                """
                for i in range(self.__steps+1):
                    aux(viewport, self.__steps, DDx_[0], DDy_[0], tk_ids)
                    for j in range(len(DDx_)-1):
                        DDx_[j] = np.array(DDx_[j]) + np.array(DDx_[j+1])
                        DDy_[j] = np.array(DDy_[j]) + np.array(DDy_[j+1])
    
        self.set_tkinter_id(tk_ids)

    def delete(self):

        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)
