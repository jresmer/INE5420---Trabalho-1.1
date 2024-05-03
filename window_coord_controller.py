from utils import Utils
import numpy as np


class WindowCoordController:

    def __init__(self, p: tuple=(250, 250), vup: tuple=(0, 250), u: tuple=(250, 0)) -> None:

        self.__origin = p
        self.__vup = vup
        self.__u = u
        self.__obj_coordinates = dict()

    @staticmethod
    def __mag(v: tuple) -> float:

        vx, vy = v
        return np.sqrt(vx ** 2 + vy ** 2)
    
    # converts world coordinates (x, y) to normalized coordinates
    def __world_to_normalized(self, coord: tuple) -> tuple:
        # translate coord in (-Wcx, -Wcy)
        dx, dy = self.__origin
        m = Utils.gen_translation_matrix(-dx, -dy)
        coord = tuple(Utils.transform(coord, m))

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
        proj_m = Utils.get_ortogonal_projection_matrix(self.__origin)
        for coord in coords:
            if coord[2] != 0:
                new_coord = Utils.transform(coord, proj_m)[:-1]
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
        x,y = vector
        if x != 0 and y != 0:
            alpha = np.arctan(abs(x)/abs(y))
        else:
            alpha = 0

        theta = Utils.get_angle(alpha, y, x)

        return theta
    
    def ortogonal_projection(self, objs: dict):
        m = Utils.get_ortogonal_projection_matrix(self.__origin)

        for name,coords in objs.items():
            new_coords = list()
            for coord in coords:
                new_coords.append(Utils.transform(coord, m))
            self.change_coords(name, new_coords)

    def move(self, dx: int, dy: int, objs: dict) -> dict:
        #TESTE
        angle_vup = self.get_angle(self.__vup)
        m = Utils.gen_rotation_matrix(np.degrees(angle_vup), 0, 0)
        dx, dy = Utils.transform((dx,dy), m)
        #FIM DO TESTE
        m = Utils.gen_translation_matrix(dx, dy)
        self.__origin = tuple(Utils.transform(self.__origin, m))

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates

    def rotate(self, angle: float, objs: dict) -> dict:

        # calculate new vup and u values (rotating them)
        angle = np.radians(angle)
        magnitude_v = self.__mag(self.__vup)
        magnitude_u = self.__mag(self.__u)

        # print("magnitudes {}, {}\n".format(magnitude_v, magnitude_u))
        
        current_angle_v = self.get_angle(self.__vup)
        current_angle_u = self.get_angle(self.__u)

        # print("current angles: \n{}\n{}\n".format(np.degrees(current_angle_v), np.degrees(current_angle_u)))
    
        new_angle_v = current_angle_v + angle
        new_angle_u = current_angle_u + angle

        # print("new angles: \n{}\n{}\n".format(np.degrees(new_angle_v), np.degrees(new_angle_u)))

        # print("vectors bfr: \n{}\n{}\n".format(self.__vup, self.__u))

        vupx = np.sin(new_angle_v) * magnitude_v
        if vupx - int(vupx) < 1E-1:
            vupx = int(vupx)
        vupy = np.cos(new_angle_v) * magnitude_v
        if vupy - int(vupy) < 1E-1:
            vupy = int(vupy)
        self.__vup = (vupx,vupy)
        ux = np.sin(new_angle_u) * magnitude_u
        if ux - int(ux) < 1E-1:
            ux = int(ux)
        uy = np.cos(new_angle_u) * magnitude_u
        if uy - int(uy) < 1E-1:
            uy = int(uy)
        self.__u = (ux, uy)
        
        # print("vectors after: \n{}\n{}\n".format(self.__vup, self.__u))

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates

    def scale(self, multiplier: float, objs: dict) -> dict:

        # calculate new vup and u values (rescaling them)
        multiplier = np.sqrt(1/(1 + multiplier)) if multiplier >= 0 else np.sqrt(1 + abs(multiplier))
        magnitude_v = self.__mag(self.__vup) * multiplier
        magnitude_u = self.__mag(self.__u) * multiplier
        angle_v = self.get_angle(self.__vup)
        angle_u = self.get_angle(self.__vup)
        self.__vup = (np.sin(angle_v) * magnitude_v,
                      np.cos(angle_v) * magnitude_v)
        self.__u = (np.sin(angle_u) * magnitude_u,
                      np.cos(angle_u) * magnitude_u)

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates
