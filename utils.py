import numpy as np
import sympy as sp
from copy import deepcopy
from singleton_meta import SingletonMeta


class Clipping(SingletonMeta):
    def __init__(self):
        self.__point_clipping = self.point_clipping
        self.__line_clipping = self.liang_barsky
        self.__polygon_clipping = self.adapted_weiler_atherton

    def get_all_line_clippings(self):
        return {"Liang-Barsky": "Liang-Barsky", "Cohen-Sutherland": "Cohen-Sutherland"}
    
    def line_clipping(self, bounderies, coordinates):
        return self.__line_clipping(bounderies, coordinates)

    def change_line_clipping(self, algorithm):
        if algorithm == "Liang-Barsky":
            self.__line_clipping = Clipping.liang_barsky
        else:
            self.__line_clipping = Clipping.cohen_sutherland

    @staticmethod
    def point_clipping(boundaries: tuple, coordinates: tuple) -> bool:

        x_min, y_min, x_max, y_max = boundaries
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
                m = y_diff / x_diff if x_diff != 0 else 0

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
                    x = x + 1/m * (y_min - y) if m != 0 else x
                    y = y_min
                    
                # if Pi is to the above of the window
                elif y_max < y:
                    x = x + 1/m * (y_max - y) if m != 0 else x
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
    def adapted_weiler_atherton(boundaries: tuple, coordinates: tuple) -> tuple:
    
        x_min, y_min, x_max, y_max = boundaries
        clipping_pol = [("p", (x_min, y_min)), ("p", (x_min, y_max)),
                        ("p", (x_max, y_max)), ("p", (x_max, y_min))]
        clipped_pol = list()
        coord_inside_pol = [False] * len(coordinates)

        # 1. List intersection points i1, i2...
        # 2. Label intersections as entering and exiting
        # 3. Create clipped polygon and clipping polygon lists
        intersections = list()
        for i in range(len(coordinates)):

            clipped_pol.append(("p", coordinates[i]))
            j = i+1 if i+1 < len(coordinates) else 0
            coord_pair = [coordinates[i], coordinates[j]]
            checking_coord_pair = deepcopy(coord_pair)
            possible_intersections = Clipping.cohen_sutherland(boundaries, coord_pair)

            if possible_intersections is None:
                possible_intersections = []

            elif possible_intersections == checking_coord_pair:
                coord_inside_pol[i] = True
                continue

            first = True
            # checks if coordinate is an intersection
            for x1, y1 in possible_intersections:
                if (x1,y1) in checking_coord_pair:
                    continue
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

        if all(coord_inside_pol):
            return coordinates

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

        visited = {intersection: intersection[0] == 'entering' for intersection in intersections}
        v = list()
        i = 0
        j = 0
        entering_point = None
        exiting_point = None
        # find an initial exiting point
        while intersections:

            type_, c = clipped_pol[i]

            if type_ == "exiting":
                
                exiting_point = (type_, c)
                break
                
            i = i + 1 if i + 1 < len(clipped_pol) else 0

        while not all(list(visited.values())):
            # find the exiting point in the clipping polygon list
            while True:

                type_, c = clipping_pol[j]
                if (type_, c) == exiting_point:

                    visited[(type_, c)] = True
                    break
            
                j = j + 1 if j + 1 < len(clipping_pol) else 0
            # iterate through clipping plygon list untill an entering point is found
            while True:

                type_, c = clipping_pol[j]

                if type_ == "entering":

                    entering_point = clipping_pol[j]
                    break

                v.append(c)
                j = j + 1 if j + 1 < len(clipping_pol) else 0
            # find the entering point in the clipped polygon list
            while True:

                type_, c = clipped_pol[i]

                if (type_, c) == entering_point:

                    break

                i = i + 1 if i + 1 < len(clipped_pol) else 0
            # iterate through clipped plygon list untill an exiting point is found
            while True:

                type_, c = clipped_pol[i]

                if type_ == "exiting":
                    
                    exiting_point = (type_, c)
                    break
                
                v.append(c)
                i = i + 1 if i + 1 < len(clipped_pol) else 0
        
        return v
    
    @staticmethod
    def curve_clipping(boundaries: tuple, coordinates: tuple) -> tuple:
        p1,p2,p3,p4 = coordinates

        ax,bx,cx,dx = Utils.get_bezier_coeficients([p1[0], p2[0], p3[0], p4[0]])
        ay,by,cy,dy = Utils.get_bezier_coeficients([p1[1], p2[1], p3[1], p4[1]])

        x_min, y_min, x_max, y_max = boundaries

        #Find intersections
        t = sp.Symbol('t', real = True)
        t_intercept = set()
        for i in sp.solveset(ax*t**3 + bx*t**2 + cx*t + dx - x_min,t):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i.is_real and i >= 0 and i <= 1 and y <= y_max and y >= y_min:
                t_intercept.add(i)

        for i in sp.solveset(ax*t**3 + bx*t**2 + cx*t + dx - x_max,t):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i.is_real and i >= 0 and i <= 1 and y <= y_max and y >= y_min:
                t_intercept.add(i)

        result = sp.solveset(ay*t**3 + by*t**2 + cy*t + dy - y_min,t)
        for i in result:
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            if i.is_real and i >= 0 and i <= 1 and x <= x_max and x >= x_min:
                t_intercept.add(i)
        
        result = sp.solveset(ay*t**3 + by*t**2 + cy*t + dy - y_max,t)
        for i in result:
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i.is_real and i >= 0 and i <= 1 and x <= x_max and x >= x_min:
                t_intercept.add(i)

        t_intercept.add(0)
        t_intercept.add(1)
        t_intercept = list(t_intercept)
        t_intercept.sort()

        coords = []

        number_of_ts = 200
        range_t = 1/number_of_ts

        #Checking if start drawing
        draw = False
        if x_min <= p1[0] and p1[0] <= x_max and y_min <= p1[1] and p1[1] <= y_max:
            draw = True

        #Calculate t for each segment
        for i in range(len(t_intercept)-1):
            
            if draw:
                segment_coords = []
                lim_if = int(t_intercept[i]*number_of_ts)
                lim_sup = int(t_intercept[i+1]*number_of_ts)
                t_to_be_calculated = [x*range_t for x in range(lim_if, lim_sup+1)]

                for t in t_to_be_calculated:

                    t_square = t*t
                    t_cubic = t_square*t
                    x = ax*t_cubic + bx*t_square + cx*t + dx
                    y = ay*t_cubic + by*t_square + cy*t + dy

                    segment_coords.append((x,y))
                coords.append(segment_coords)
            draw = not draw

        return coords


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
    def get_bezier_coeficients(ps: list):
        m = np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 3, 0, 0],
                      [1, 0, 0, 0]])
        
        p1, p2, p3, p4 = ps
        return np.matmul(m, [p1,p2,p3,p4])

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
