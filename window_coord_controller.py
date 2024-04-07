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
        vupx, vupy = self.__vup

        # sig_vupx = 1 if vupx >= 0 else -1
        # sig_vupy = 1 if vupy >= 0 else -1
        
        if vupy != 0:
            alpha = np.arctan(vupx/vupy)
        else:
            alpha = 0

        # with the magic of math
        # theta = np.pi * 3 / 4 + (np.pi / 4) * sig_vupx + (sig_vupx/sig_vupy) * alpha
        # with if / else:
        theta = 0
        if vupx > 0 and vupy > 0:
            theta = np.pi + alpha
        elif vupx > 0 and vupy < 0:
            theta = np.pi - alpha
        elif vupx < 0 and vupy > 0:
            theta = np.pi / 2 - alpha
        elif vupx < 0 and vupy < 0:
            theta = np.pi / 2 + alpha
        m = Utils.gen_rotation_matrix(
            angle=theta,
            cx=dx,
            cy=dy
        )
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
        
        # converts coordinates to the window appropriate format
        for coord in coords:
            new_coord = self.__world_to_normalized(coord)
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
    
    def move(self, dx: int, dy: int, objs: dict) -> dict:

        m = Utils.gen_translation_matrix(dx, dy)
        self.__origin = tuple(Utils.transform(self.__origin, m))

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
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
            self.change_coords(name, coords)
        
        return self.__obj_coordinates

    def scale(self, multiplier: float, objs: dict) -> dict:

        # calculate new vup and u values (rescaling them)
        multiplier = np.sqrt(1/(1 + multiplier)) if multiplier >= 0 else np.sqrt(1 + abs(multiplier))
        print(multiplier)
        magnitude_v = self.__mag(self.__vup) * multiplier
        magnitude_u = self.__mag(self.__u) * multiplier
        vupx, vupy = self.__vup
        angle_v = np.arctan(vupx / vupy) if vupy != 0 else 0
        ux, uy = self.__u
        angle_u = np.arctan(ux / uy) if uy != 0 else 0
        self.__vup = (np.sin(angle_v) * magnitude_v,
                      np.cos(angle_v) * magnitude_v)
        self.__u = (np.sin(angle_u) * magnitude_u,
                      np.cos(angle_u) * magnitude_u)
        print(self.__vup)
        print(self.__u)

        for name in objs.keys():

            coords = objs[name]
            self.change_coords(name, coords)
        
        return self.__obj_coordinates
