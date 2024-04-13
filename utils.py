import numpy as np


class Clippling:

    @staticmethod
    def point_clipping(bounderies: tuple, coordinates: tuple) -> bool:

        x_min, y_min, x_max, y_max = bounderies
        x, y = coordinates

        return x_min < x and x < x_max and y_min < y and y < y_max
    
    @staticmethod
    def cohen_sutherland(bounderies: tuple, coordinates: tuple) -> tuple:

        x_min, y_min, x_max, y_max = bounderies
        rc = [[0, 0, 0, 0],
              [0, 0, 0, 0]]
        i = 0
        for x, y in coordinates:

            if x < x_min: rc[i][3] = 1
            if x > x_max: rc[i][2] = 1
            if y < y_min: rc[i][1] = 1
            if y > y_max: rc[i][0] = 1

            i += 1

        # RC0 & RC1 <> [0 0 0 0]
        rc1_rc2 = any([a and b for a, b in zip(rc[0], rc[1])])

        # line is totally visible: RC0 = RC1 = [0 0 0 0]
        if rc[0] == rc[1] and not any(rc[0]):

            return coordinates
        # line is totally out of window: RC0 & RC1 <> [0 0 0 0]
        elif rc1_rc2:

            return None
        # line is partially visible: RC0 <> RC1, RC0 & RC1 = [0 0 0 0]
        elif rc[0] != rc[1] and not rc1_rc2:
            
            for i in range(2):

                x, y = coordinates[i]

                x1, y1 = coordinates[0] if i == 1 else coordinates[1]
                x_diff = x - x1
                y_diff = y - y1
                m = y_diff / x_diff

                # if Pi is to the left of the window
                if x < x_min:
                    
                    x = x_min
                    y = m * (x_min - x) + y
                # if Pi is to the right of the window
                elif x_max < x:

                    x = x_max
                    y = m * (x_max - x) + y
                
                # if Pi is to the below of the window
                if y < y_min:
                    
                    y = y_min
                    x = x + 1/m * (y_min - y)
                # if Pi is to the above of the window
                elif y_max < y:

                    y = y_max
                    x = x + 1/m * (y_max - y)

                coordinates[i] = (x, y)

            return coordinates
                    
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
    def gen_simple_rotation_matrix(angle: float) -> np.array:

        angle = np.radians(angle)
        cos_teta = np.cos(angle)
        sen_teta = np.sin(angle)

        m = np.array([[cos_teta,   -sen_teta,   0],
                        [sen_teta,   cos_teta,   0],
                        [0,   0,    1]])
        
        return m
    
    @staticmethod
    def transform(coord: tuple, m: np.array) -> list:

        coord = np.array(coord + (1,))
        coord = np.matmul(coord, m)
        coord.tolist()
        return coord[:-1]
