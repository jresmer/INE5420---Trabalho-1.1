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
        m = Utils.gen_translation_matrix(dx, dy)
        coord = Utils.transform(coord, m)

        # rotate coord in -θ(Y, vup)
        vupx, vupy = self.__vup
        alpha = np.arctan(vupy / vupx)
        # with the magic of math
        theta = np.pi * 3 / 4 + (np.pi / 4) * (abs(vupx)/vupx) + (vupx/vupy) * alpha
        # with if / else:
        # if vupx > 0 and vupy > 0:
        #     theta = np.pi + alpha
        # elif vupx > 0 and vupy < 0:
        #     theta = np.pi - alpha
        # elif vupx < 0 and vupy > 0:
        #     theta = np.pi / 2 - alpha
        # elif vupx < 0 and vupy < 0:
        #     theta = np.pi / 2 + alpha
        m = Utils.gen_rotation_matrix(
            angle=theta,
            cx=dx,
            cy=dy
        )
        coord = Utils.transform(coord, m)

        # normalize coord
        y_max = self.__mag(self.__vup)
        x_max = self.__mag(self.__u)
        x, y = coord
        x_diff = x + x_max
        y_diff = y + y_max
        new_x = x_diff / (2 * x_max)
        new_y = y_diff / (2* y_max)
        
        return new_x, new_y

    def get_origin(self) -> tuple:

        return self.__origin
    
    def set_dimensions(self, new_origin: tuple) -> None:

        self.__origin = new_origin
    
    # adds new obj coordinates 
    def add_obj(self, name: str, coords: tuple) -> bool:

        if name not in self.__obj_coordinates.keys():

            new_coords = list()
        
            # converts coordinates to the window appropriate format
            for coord in coords:

                new_coord = self.__world_to_normalized(coords)
                new_coords.append(new_coord)

            self.__obj_coordinates[name] = new_coords

            return True

        else:

            return False

    def get_coods(self) -> dict:

        return self.__obj_coordinates
    
    def move(self, dx: int, dy: int, objs: dict) -> dict:

        m = Utils.gen_translation_matrix(dx, dy)
        self.__origin = Utils.transform(self.__origin, m)

        for name in objs.keys():

            coords = objs[name]
            new_coords = list()

            for coord in coords:
                new_coord = self.__world_to_normalized(coord)
                new_coords.append(new_coord)

            self.__obj_coordinates[name] = coords
        
        return self.__obj_coordinates

    def rotate(self, angle: float, objs: dict) -> dict:

        # calculate new vup and u values (rotating them)
        magnitude_v = self.__mag(self.__vup)
        magnitude_u = self.__mag(self.__u)
        vupx, vupy = self.__vup
        current_angle_v = np.arctan(vupy / vupx)
        ux, uy = self.__u
        current_angle_u = np.arctan(uy / ux)
        new_angle_v = current_angle_v + angle
        new_angle_u = current_angle_u + angle
        self.__vup = (np.sin(new_angle_v) * magnitude_v,
                      np.cos(new_angle_v) * magnitude_v)
        self.__u = (np.sin(new_angle_u) * magnitude_u,
                      np.cos(new_angle_u) * magnitude_u)

        for name in objs.keys():

            coords = objs[name]
            new_coords = list()

            for coord in coords:
                new_coord = self.__world_to_normalized(coord)
                new_coords.append(new_coord)

            self.__obj_coordinates[name] = coords
        
        return self.__obj_coordinates

    def scale(self, multiplier: float, objs: dict) -> dict:

        # calculate new vup and u values (rescaling them)
        multiplier = np.sqrt(multiplier)
        magnitude_v = self.__mag(self.__vup) * multiplier
        magnitude_u = self.__mag(self.__u) * multiplier
        vupx, vupy = self.__vup
        angle_v = np.arctan(vupy / vupx)
        ux, uy = self.__u
        angle_u = np.arctan(uy / ux)
        self.__vup = (np.sin(angle_v) * magnitude_v,
                      np.cos(angle_v) * magnitude_v)
        self.__u = (np.sin(angle_u) * magnitude_u,
                      np.cos(angle_u) * magnitude_u)

        for name in objs.keys():

            coords = objs[name]
            new_coords = list()

            for coord in coords:
                new_coord = self.__world_to_normalized(coord)
                new_coords.append(new_coord)

            self.__obj_coordinates[name] = coords
        
        return self.__obj_coordinates
