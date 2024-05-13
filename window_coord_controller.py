from utils import Utils
import numpy as np


class WindowCoordController:

    def __init__(self, p: tuple=(250, 250, 0), vup: tuple=(0, 250, 0), u: tuple=(250, 0), vpn: tuple=(0, 0, 250)) -> None:

        self.__origin = p
        self.__vup = vup
        self.__u = u
        self.__vpn = vpn
        self.__obj_coordinates = dict()
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.__proj_m = Utils.get_ortogonal_projection_matrix(self.__origin, self.angleX, self.angleY)

    @staticmethod
    def __mag(v: tuple) -> float:

        sum_ = 0
        for comp in v:

            sum_ += comp**2

        return np.sqrt(sum_)
    
    def __recalculate_projection_matrix(self):

        self.__proj_m = Utils.get_ortogonal_projection_matrix(self.__origin, self.angleX, self.angleY)
    
    # converts world coordinates (x, y) to normalized coordinates
    def __world_to_normalized(self, coord: tuple) -> tuple:

        dx, dy, _ = self.__origin

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
            x,y,z = tuple(Utils.transform(coord, self.__proj_m))
            new_coord = self.__world_to_normalized((x,y))

            # check if out of field of vision
            vpn_magnitude = self.__mag(self.__vpn)
            if (z >= 0 and z > 3*vpn_magnitude) or (z < 0 and abs(z) > vpn_magnitude):
                new_coords = []
                break

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
    
    def update_coordinates(self, objs: dict):
        for name, coords in objs.items():
            self.change_coords(name, coords)
    
    def move(self, dx: int, dy: int, dz: int, objs: dict) -> dict:

        # rotate the translation vector to respect vup
        m = Utils.rotation_to_y_axis_matrix((self.__origin, self.__vup))
        dx, dy, dz = Utils.transform((dx, dy, dz), m)

        # translate the origin
        m = Utils.gen_3d_translation_matrix(dx, dy, dz)
        self.__origin = tuple(Utils.transform(self.__origin, m))

        self.__recalculate_projection_matrix()
        self.update_coordinates(objs)
        
        return self.__obj_coordinates

    def rotate(self, axis: str, angle: float, objs: dict) -> dict:

        if axis == "x":
            a = (1, 0, 0)
            self.angleX = (self.angleX + angle) %360
        elif axis == "y": 
            a = (0, 1, 0)
            self.angleY = (self.angleY + angle) %360
        elif axis == "z":
            a = (0, 0, 1)
            self.angleZ = (self.angleZ + angle) %360

        m = Utils.gen_3d_rotation_matrix(angle, ((0,0,0), a))
        self.__vup = tuple(Utils.transform(self.__vup, m))
        self.__u = tuple(Utils.transform(self.__u, m))
        self.__vpn = tuple(Utils.transform(self.__vpn, m))

        self.__recalculate_projection_matrix()
        self.update_coordinates(objs)
        
        return self.__obj_coordinates

    def scale(self, multiplier: float, objs: dict) -> dict:

        # calculate new vup and u values (rescaling them)
        multiplier = np.sqrt(1/(1 + multiplier)) if multiplier >= 0 else np.sqrt(1 + abs(multiplier))
        m = Utils.gen_3d_scaling_matrix(multiplier, multiplier, multiplier,0,0,0)
        self.__vup = tuple(Utils.transform(self.__vup, m))
        self.__u = tuple(Utils.transform(self.__u, m))
        self.__vpn = tuple(Utils.transform(self.__vpn, m))

        self.__recalculate_projection_matrix()
        self.update_coordinates(objs)
        
        return self.__obj_coordinates