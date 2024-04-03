from singleton_meta import SingletonMeta


class WindowCoordController:

    def __init__(self, d: tuple) -> None:

        self.__dimensions = d
        self.__obj_coordinates = dict()
    
    # converts world coordinates (x, y) to normalized coordinates
    def __world_to_normalized(self, coord: tuple) -> tuple:

        ...

    def get_dimensions(self) -> tuple:

        return self.__dimensions
    
    def set_dimensions(self, new_d: tuple) -> None:

        self.__dimensions = new_d
    
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
