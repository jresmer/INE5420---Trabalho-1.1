from utils import Utils
import numpy as np


class WindowCoordController:

    def __init__(self, p: tuple=(250, 250), vup: tuple=(0, 250), u: tuple=(250, 0)) -> None:

        self.__origin = p
        self.__vup = vup
        self.__u = u
        self.__obj_coordinates = dict()
        self.__proj_m = Utils.get_ortogonal_projection_matrix(self.__origin)

    @staticmethod
    def __mag(v: tuple) -> float:

        sum_ = 0
        for comp in v:

            sum_ += comp**2

        return np.sqrt(sum_)
    
    def __recalculate_projection_matrix(self):

        self.__proj_m = Utils.get_ortogonal_projection_matrix(self.__origin)
    
    # converts world coordinates (x, y) to normalized coordinates
    def __world_to_normalized(self, coord: tuple) -> tuple:
        # translate coord in (-Wcx, -Wcy)
        dx, dy, z = self.__origin
        # m = Utils.gen_translation_matrix(0, 0)

        # coord = tuple(Utils.transform(coord, m))

        # rotate coord in -θ(Y, vup)
        theta = self.get_angle(self.__vup)
        m = Utils.gen_simple_rotation_matrix(np.degrees(-theta))
        coord = tuple(Utils.transform(coord, m))

        # normalize coord
        y_max = self.__mag(self.__vup)
        x_max = self.__mag(self.__u)
        x, y = coord
        new_x = x / (x_max)
        new_y = y / (y_max)

        return (new_x, new_y)

    def get_origin(self) -> tuple:

        return self.__origin
    
    def set_dimensions(self, new_origin: tuple) -> None:

        self.__origin = new_origin
    
    def att_obj(self, name: str, coords: tuple) -> None:
        if name in self.__obj_coordinates.keys():

            self.change_coords(name, coords)

            return True

        else:
            return False
    
    def change_coords(self, name: str, coords: tuple) -> None:
        new_coords = list()
        for coord in coords:
            new_coord = tuple(Utils.transform(coord, self.__proj_m)[:-1])
            new_coord = self.__world_to_normalized(new_coord)
            new_coords.append(new_coord)

        self.__obj_coordinates[name] = new_coords

    # adds new obj coordinates 
    def add_obj(self, name: str, coords: tuple) -> bool:
        if name not in self.__obj_coordinates.keys():
            self.change_coords(name, coords)
            return True
        else:
            return False

    def get_coords(self) -> dict:

        return self.__obj_coordinates
    
    def get_angle(self, vector: tuple) -> float:
        x,y,z = vector
        if x != 0 and y != 0:
            alpha = np.arctan(abs(x)/abs(y))
        else:
            alpha = 0

        theta = Utils.get_angle(alpha, y, x)

        return theta
    
    def move(self, dx: int, dy: int, dz: int, objs: dict) -> dict:

        # rotate the translation vector to respect vup
        m = Utils.rotation_to_y_axis_matrix((self.__origin, self.__vup))
        dx, dy, dz = Utils.transform((dx, dy, dz), m)

        # translate the origin
        m = Utils.gen_3d_translation_matrix(dx, dy, dz)
        self.__origin = tuple(Utils.transform(self.__origin, m))

        self.__recalculate_projection_matrix()

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates

    # TODO - add axis parameter
    def rotate(self, angle: float, objs: dict) -> dict:

        # TODO - temporário
        axis = "y"

        if axis == "x":
            a = (1, 0, 0)
        elif axis == "y": 
            a = (0, 1, 0)
        elif axis == "z":
            a = (0, 0, 1)

        m = Utils.gen_3d_rotation_matrix(angle, (self.__origin, a))
        self.__vup = tuple(Utils.transform(self.__vup, m))
        self.__u = tuple(Utils.transform(self.__u, m))

        self.__recalculate_projection_matrix()

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates

    def scale(self, multiplier: float, objs: dict) -> dict:

        # calculate new vup and u values (rescaling them)
        multiplier = np.sqrt(1/(1 + multiplier)) if multiplier >= 0 else np.sqrt(1 + abs(multiplier))
        m = Utils.gen_3d_scaling_matrix(multiplier,
                                        multiplier,
                                        multiplier,
                                        self.__origin[0],
                                        self.__origin[1],
                                        self.__origin[2])
        self.__vup = tuple(Utils.transform(self.__vup, m))
        self.__u = tuple(Utils.transform(self.__u, m))

        self.__recalculate_projection_matrix()

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates
