from utils import Utils
import numpy as np


class WindowCoordController:

    def __init__(self, p: tuple=(250, 250), vup: tuple=(0, 250), u: tuple=(250, 0)) -> None:

        self.__origin = p
        self.__vup = vup
        self.__u = u
        self.__obj_coordinates = dict()
    
    # converts world coordinates (x, y) to normalized coordinates
    def __world_to_normalized(self, coord: tuple) -> tuple:

        def mag(v: tuple) -> float:

            vx, vy = v
            return np.sqrt(vx ** 2 + vy ** 2)

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
        y_max = mag(self.__vup)
        x_max = mag(self.__u)
        x, y = coord
        x_diff = x + x_max
        y_diff = y + y_max
        new_x = x / (2 * x_max)
        new_y = y / (2* y_max)
        
        return new_x, new_y

    def get_origin(self) -> tuple:

        return self.__origin
    
    def set_dimensions(self, new_origin: tuple) -> None:

        self.__origin = new_origin
    
    # adds new obj coordinates 
    def add_obj(self, name: str, coords: tuple) -> bool:

        if name not in self.__obj_coordinates.keys():
        
            # converts coordinates to the window appropriate format
            coords = self.__world_to_normalized(coords)
            self.__obj_coordinates[name] = coords

            return True

        else:

            return False

    def get_coods(self) -> dict:

        return self.__obj_coordinates
    
    def move(self, dx: int, dy: int) -> list:

        ...

    def rotate(self, angle: float) -> list:

        ...

    def scale(self, pct: float) -> list:

        ...
