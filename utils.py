import numpy as np


class Utils:

    @staticmethod
    def gen_translation_matrix(dx: int, dy: int) -> np.array:
    
        m = [[1, 0, 0],
             [0, 1, 0],
             [dx, dy, 1]]
        
        return np.array(m)
    
    @staticmethod
    def gen_scaling_matrix(sx: int, sy: int, cx: int, cy: int) -> np.array:

        m1 = np.array([[1,   0,   0],
                        [0,   1,   0],
                        [-cx, -cy, 1]])
        m2 = np.array([[sx,   0,   0],
                        [0,   sy,   0],
                        [0,   0,    1]])
        m3 = np.array([[1,   0,   0],
                        [0,   1,   0],
                        [cx, cy,   1]])
            
        m = np.matmul(m1,m2)
        m = np.matmul(m, m3)

        return m
    
    @staticmethod
    def gen_rotation_matrix(angle: float, cx: int, cy: int) -> np.array:

        angle = np.radians(angle)
        cos_teta = np.cos(angle)
        sen_teta = np.sin(angle)

        m1 = np.array([[1,   0,   0],
                        [0,   1,   0],
                        [-cx, -cy, 1]])
        m2 = np.array([[cos_teta,   -sen_teta,   0],
                        [sen_teta,   cos_teta,   0],
                        [0,   0,    1]])
        m3 = np.array([[1,   0,   0],
                        [0,   1,   0],
                        [cx, cy,   1]])
            
        m = np.matmul(m1,m2)
        m = np.matmul(m, m3)

        return m
    
    @staticmethod
    def transform(coord: tuple, m: np.array) -> list:

        coord = np.array(coord + (1,))
        coord = np.matmul(coord, m)
        coord.tolist()
        return coord[:-1]

    @staticmethod
    def get_angle(vector: tuple) -> float:
        x,y = vector
        if x != 0 and y != 0:
            alpha = np.arctan(abs(x)/abs(y))
        elif x != 0 and y == 0:
            alpha = np.pi/2
        else:
            alpha = 0

        theta = 0
        if x != 0 and y == 0:
            theta = np.pi/2 if y > 0 else 3*np.pi/2
        elif x == 0 and y < 0:
            theta = np.pi

        elif x > 0 and y > 0:
            theta = alpha
        elif x < 0 and y > 0:
            theta = -alpha
        elif x > 0 and y < 0:
            theta = np.pi - alpha
        elif x < 0 and y < 0:
            theta = np.pi + alpha
        return theta