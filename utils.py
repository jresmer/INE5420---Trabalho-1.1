import numpy as np
import math
from copy import deepcopy
from singleton_meta import SingletonMeta

class CubicEquationSolver:
    # CUBIC ROOT SOLVER

    # Date Created   :    24.05.2017
    # Created by     :    Shril Kumar [(shril.iitdhn@gmail.com),(github.com/shril)] &
    #                     Devojoyti Halder [(devjyoti.itachi@gmail.com),(github.com/devojoyti)]

    # Project        :    Classified 
    # Use Case       :    Instead of using standard numpy.roots() method for finding roots,
    #                     we have implemented our own algorithm which is ~10x faster than
    #                     in-built method.

    # Algorithm Link :    www.1728.org/cubic2.htm

    # This script (Cubic Equation Solver) is an independent program for computation of roots of Cubic Polynomials. This script, however,
    # has no relation with original project code or calculations. It is to be also made clear that no knowledge of it's original project 
    # is included or used to device this script. This script is complete freeware developed by above signed users, and may further be
    # used or modified for commercial or non-commercial purpose.


    # Libraries imported for fast mathematical computations.
    # import math
    # import numpy as np

    # Main Function takes in the coefficient of the Cubic Polynomial
    # as parameters and it returns the roots in form of numpy array.
    # Polynomial Structure -> ax^3 + bx^2 + cx + d = 0
    
    @staticmethod
    def solve(a, b, c, d):

        # Helper function to return float value of f.
        def findF(a, b, c):
            return ((3.0 * c / a) - ((b ** 2.0) / (a ** 2.0))) / 3.0


        # Helper function to return float value of g.
        def findG(a, b, c, d):
            return (((2.0 * (b ** 3.0)) / (a ** 3.0)) - ((9.0 * b * c) / (a **2.0)) + (27.0 * d / a)) /27.0


        # Helper function to return float value of h.
        def findH(g, f):
            return ((g ** 2.0) / 4.0 + (f ** 3.0) / 27.0)

        if (a == 0 and b == 0):                   # Case for handling Liner Equation
            if c == 0: return np.array([d])
            return np.array([(-d * 1.0) / c])                 # Returning linear root as numpy array.

        elif (a == 0):                              # Case for handling Quadratic Equations

            D = c * c - 4.0 * b * d                       # Helper Temporary Variable
            if D >= 0:
                D = math.sqrt(D)
                x1 = (-c + D) / (2.0 * b)
                x2 = (-c - D) / (2.0 * b)
            else:
                D = math.sqrt(-D)
                x1 = (-c + D * 1j) / (2.0 * b)
                x2 = (-c - D * 1j) / (2.0 * b)
                
            return np.array([x1, x2])               # Returning Quadratic Roots as numpy array.

        f = findF(a, b, c)                          # Helper Temporary Variable
        g = findG(a, b, c, d)                       # Helper Temporary Variable
        h = findH(g, f)                             # Helper Temporary Variable

        if f == 0 and g == 0 and h == 0:            # All 3 Roots are Real and Equal
            if (d / a) >= 0:
                x = (d / (1.0 * a)) ** (1 / 3.0) * -1
            else:
                x = (-d / (1.0 * a)) ** (1 / 3.0)
            return np.array([x, x, x])              # Returning Equal Roots as numpy array.

        elif h <= 0:                                # All 3 roots are Real

            i = math.sqrt(((g ** 2.0) / 4.0) - h)   # Helper Temporary Variable
            j = i ** (1 / 3.0)                      # Helper Temporary Variable
            k = math.acos(-(g / (2 * i)))           # Helper Temporary Variable
            L = j * -1                              # Helper Temporary Variable
            M = math.cos(k / 3.0)                   # Helper Temporary Variable
            N = math.sqrt(3) * math.sin(k / 3.0)    # Helper Temporary Variable
            P = (b / (3.0 * a)) * -1                # Helper Temporary Variable

            x1 = 2 * j * math.cos(k / 3.0) - (b / (3.0 * a))
            x2 = L * (M + N) + P
            x3 = L * (M - N) + P

            return np.array([x1, x2, x3])           # Returning Real Roots as numpy array.

        elif h > 0:                                 # One Real Root and two Complex Roots
            R = -(g / 2.0) + math.sqrt(h)           # Helper Temporary Variable
            if R >= 0:
                S = R ** (1 / 3.0)                  # Helper Temporary Variable
            else:
                S = (-R) ** (1 / 3.0) * -1          # Helper Temporary Variable
            T = -(g / 2.0) - math.sqrt(h)
            if T >= 0:
                U = (T ** (1 / 3.0))                # Helper Temporary Variable
            else:
                U = ((-T) ** (1 / 3.0)) * -1        # Helper Temporary Variable

            x1 = (S + U) - (b / (3.0 * a))
            # x2 = -(S + U) / 2 - (b / (3.0 * a)) + (S - U) * math.sqrt(3) * 0.5j
            # x3 = -(S + U) / 2 - (b / (3.0 * a)) - (S - U) * math.sqrt(3) * 0.5j
            
            return np.array([x1])           # Returning One Real Root and two Complex Roots as numpy array.


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
    def curve_clipping(boundaries: tuple, coordinates: tuple, coeficients_x, coeficients_y) -> tuple:
        p1,p2,p3,p4 = coordinates
        ax,bx,cx,dx = coeficients_x
        ay,by,cy,dy = coeficients_y
        x_min, y_min, x_max, y_max = boundaries


        #Verificando casca
        min_y = y_max + 1
        max_y = y_min - 1
        min_x = x_max + 1
        max_x = x_min - 1
        for (x,y) in [p1,p2,p3,p4]:
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x 

            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y  
        
        coords_casca = [[(min_x, min_y), (min_x, max_y)], 
                        [(min_x, max_y), (max_x, max_y)] ,
                        [(max_x, max_y), (max_x,min_y)], 
                        [(max_x,min_y), (min_x, min_y)]]

        casca_inside = []
        for line in coords_casca:
            casca_inside.append(Clipping.cohen_sutherland(boundaries, line) != None)

        #If all points inside viewport, there are no intersections to calculate
        if all(casca_inside):
            return [0,1]
        
        #If all points outside, dont have to draw
        if not any(casca_inside):
            return []

        #Find intersections
        # t = sp.Symbol('t', real = True)
        t_intercept = set()
        for i in CubicEquationSolver.solve(ax,bx,cx,dx-x_min):#sp.solveset(ax*t**3 + bx*t**2 + cx*t + dx - x_min,t):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and y <= y_max and y >= y_min:
                t_intercept.add(i)

        for i in CubicEquationSolver.solve(ax,bx,cx,dx-x_max):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and y <= y_max and y >= y_min:
                t_intercept.add(i)

        for i in CubicEquationSolver.solve(ay,by,cy,dy-y_min):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            if i >= 0 and i <= 1 and x <= x_max and x >= x_min:
                t_intercept.add(i)
        
        for i in CubicEquationSolver.solve(ay,by,cy,dy-y_max):
            x = ax*i**3 + bx*i**2 + cx*i + dx
            y = ay*i**3 + by*i**2 + cy*i + dy
            
            if i >= 0 and i <= 1 and x <= x_max and x >= x_min:
                t_intercept.add(i)

        t_intercept.add(0)
        t_intercept.add(1)
        t_intercept = list(t_intercept)
        t_intercept.sort()

        return t_intercept


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
    
    def get_bspline_coeficients(ps: list):
        m = np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 0, 3, 0],
                      [1, 4, 1, 0]])
        m = m/6
        
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
