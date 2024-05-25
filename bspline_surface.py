from canvas_object import CanvasObject
from utils import Utils, Clipping
from copy import deepcopy
import numpy as np


class BsplineSurface(CanvasObject):

    def __init__(self, coord: tuple, color: str, name: str, tkinter_id: int, canvas) -> None:

        new_coords = []
        if len(coord) > 0 and type(coord[0]) == list:

            matrix_created = []
            #Linearizando a matriz e tratando encontro de retalhos
            for i in range(4):
                matrix_created.append([False,False,False,False])
                for j in range(4):
                    line1 = coord[i*4    ][j*4:(j+1)*4]
                    line2 = coord[i*4 + 1][j*4:(j+1)*4]
                    line3 = coord[i*4 + 2][j*4:(j+1)*4]
                    line4 = coord[i*4 + 3][j*4:(j+1)*4]
                    matrix = line1+line2+line3+line4
                    
                    if all([a == None for a in matrix]):
                        continue

                    if None in matrix:
                        self.set_invalid()
                        return
                    else:

                        if i > 0 and matrix_created[i-1][j]:
                            line1 = coord[i*4-1][j*4:(j+1)*4]
                        if j > 0 and matrix_created[i][j-1]: 
                            line1[0] = coord[i*4][j*4-1]
                            line2[0] = coord[i*4 + 1][j*4-1]
                            line3[0] = coord[i*4 + 2][j*4-1]
                            line4[0] = coord[i*4 + 3][j*4-1]

                        matrix = line1 + line2 + line3 + line4          
                        new_coords += matrix
                        matrix_created[i][j] = True
        else:
            new_coords = coord[:]
            
        for point in new_coords:
            if len(point) != 3:
                self.set_invalid()
                return
        
        super().__init__(new_coords, color, name, tkinter_id, canvas)   

        self.__steps = 100

    def draw(self, viewport: tuple, window_coords: tuple, zoom: float) -> None:

        def aux(n, DDx_row, DDy):

            ...
        
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
                Gx[i][j] = self.get_coord()[i*4+j][0]
                Gy[i][j] = self.get_coord()[i*4+j][1]

        m = Utils.get_m_bspline()
        mt = np.transpose(m)
        Cx = np.matmul(m, np.matmul(Gx, mt))
        Cy = np.matmul(m, np.matmul(Gy, mt))

        # clipping
        t_intercept = Clipping.curve_clipping(viewport, self.get_coord(), Cx, Cy)

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
        DDx_, DDy_ = deepcopy(DDx), deepcopy(DDy)

        """
        5. Draw the curve family in t
        """

    
    def delete(self):
        for line in self.get_tkinter_id():
            self.get_canvas().delete(line)
