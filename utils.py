import numpy as np
from copy import deepcopy


class Clipping:

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
                    y = m * (x_min - x) + y
                    x = x_min
                # if Pi is to the right of the window
                elif x_max < x:
                    y = m * (x_max - x) + y
                    x = x_max
                # if Pi is to the below of the window
                if y < y_min:
                    x = x + 1/m * (y_min - y)
                    y = y_min
                    
                # if Pi is to the above of the window
                elif y_max < y:
                    x = x + 1/m * (y_max - y)
                    y = y_max

                coordinates[i] = (x, y)

            return coordinates

    @staticmethod
    def liang_barsky(bounderies: tuple, coordinates: tuple) -> tuple:
        (x1,y1), (x2,y2) = coordinates
        x_min,y_min, x_max,y_max = bounderies

        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
        t_enter = 0.0
        t_exit = 1.0

        for i in range(4):
            if p[i] == 0:  # Check if line is parallel to the clipping boundary
                if q[i] < 0:
                    return None  # Line is outside and parallel, so completely discarded
            else:
                t = q[i] / p[i]
                if p[i] < 0:
                    if t > t_enter:
                        t_enter = t
                else:
                    if t < t_exit:
                        t_exit = t

        if t_enter > t_exit:
            return None  # Line is completely outside

        x1_clip = x1 + t_enter * dx
        y1_clip = y1 + t_enter * dy
        x2_clip = x1 + t_exit * dx
        y2_clip = y1 + t_exit * dy

        return (x1_clip, y1_clip), (x2_clip, y2_clip)

    @staticmethod
    def weiler_atherton(bounderies: tuple, coordinates: tuple) -> tuple:
    
        x_min, y_min, x_max, y_max = bounderies
        clipping_pol = [("p", (x_min, y_min)), ("p", (x_min, y_max)),
                        ("p", (x_max, y_max)), ("p", (x_max, y_min))]
        clipped_pol = list()

        # 1. List intersection points i1, i2...
        # 2. Label intersections as entering and exiting
        # 3. Create clipped polygon and clipping polygon lists
        intersections = list()
        for i in range(len(coordinates)):

            clipped_pol.append(("p", coordinates[i]))
            j = i+1 if i+1 < len(coordinates) else 0
            coord_pair = [coordinates[i], coordinates[j]]
            possible_intersections = Clipping.cohen_sutherland(bounderies, coord_pair)
            if possible_intersections is None:
                possible_intersections = []
            first = True
            # checks if coordinate is an intersection
            for x1, y1 in possible_intersections:

                # if (x1, y1) is an intersections
                if x1 == x_min or x1 == x_max \
                    or y1 == y_min or y1 == y_max:

                    # if p1 is out of vision
                    x, y = coordinates[i]
                    if x < x_min or x > x_max \
                        or y < y_min or y > y_max:
                        # if (x1, y1) is the first found intersection for this line
                        if first:
                            # (x1, y1) is an entering intersection
                            intersections.append(("entering", (x1, y1)))
                            clipped_pol.append(("entering", (x1, y1)))
                            first = False
                        # (x1, y1) is an exiting intersection
                        else:
                            
                            intersections.append(("exiting", (x1, y1)))
                            clipped_pol.append(("exiting", (x1, y1)))
                    # if p1 is in vision
                    else:

                        intersections.append(("exiting", (x1, y1)))
                        clipped_pol.append(("exiting", (x1, y1)))

        # 3. Create clipped polygon and clipping polygon lists
        for type_, coord in intersections:

            x, y = coord

            # intersection between (x_max, y_max) and (x_min, y_max)
            if y == y_max:

                i = clipping_pol.index(("p", (x_max, y_max)))
            # intersection between
            elif y == y_min:

                i = len(clipping_pol)
            # intersection between
            elif x == x_min:
                
                i = clipping_pol.index(("p", (x_min, y_max)))
            # intersection between
            elif x == x_max:

                i = clipping_pol.index(("p", (x_max, y_min)))

            clipping_pol = clipping_pol[:i] + [(type_, (x, y))] + clipping_pol[i:]

        visited = {intersection: intersection[0] != 'entering' for intersection in intersections}
        resulting_polygon = list()
        while not all(list(visited.values())):
            # choose the first entering intersection from clipped pol
            i = 0
            entering_point = None
            type_ = "p"
            while True:

                type_, c = clipped_pol[i]

                if type_ == "entering" and not visited[(type_, c)]:

                    entering_point = clipped_pol[i]
                    visited[(type_, c)] = True
                    break

                i = i + 1 if i + 1 < len(clipped_pol) else 0
            i = i + 1 if i + 1 < len(clipped_pol) else 0
            # iterate through clipped pol untill an exiting intersection is found
            v = list()
            exiting_point = None
            while True:

                type_, c = clipped_pol[i]
                v.append(c)

                if type_ == "exiting":

                    exiting_point = clipped_pol[i]
                    break

                i = i + 1 if i + 1 < len(clipped_pol) else 0
            # find the exiting point in the clipping pol list
            p = None
            j = -1
            while True:

                j = j + 1 if j + 1 < len(clipping_pol) else 0

                if clipping_pol[j] == exiting_point:

                    break
            
            while True:

                j = j + 1 if j + 1 < len(clipping_pol) else 0

                if (type_, c) == entering_point:

                    break

                type_, c = clipping_pol[j]
                v.append(c)
            
            resulting_polygon.append(v)
        
        return resulting_polygon


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
