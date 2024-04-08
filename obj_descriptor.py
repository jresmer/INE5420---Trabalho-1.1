from canvas_object import CanvasObject
from canvas_object_manager import CanvasObjectManager


class OBJDescriptor:

    @staticmethod
    def obj_to_wavefront(obj: CanvasObject, path: str, overwrite: bool=True) -> None:

        # writes string with obj's data
        name = obj.get_name()
        coords = obj.get_coord()
        color = obj.get_color()

        data = "o {}\n".format(name)
        data += "t {}\n".format(obj.__class__.__name__)
        data += "c {}\n".format(color)
        aux_data = ""

        for i, coord in enumerate(coords):
            coord = list(coord)
            if len(coord) < 3:

                while len(coord) < 3:

                    coord.append(1)
            
            x, y, z = coord
            coord_data = "v {} {} {}\n".format(x, y, z)
            data += coord_data

            next_coord = i + 2 if i + 2 < len(coords) else 1
            aux_data += "| {} {}\n".format(i + 1, next_coord)

        data += aux_data + "\n"

        # writes on the respective file
        mode = "wt" if overwrite else "at"
        with open(path, mode) as file:

            file.write(data)

    @staticmethod
    def wavefront_to_obj(path: str) -> tuple:
        
        ...