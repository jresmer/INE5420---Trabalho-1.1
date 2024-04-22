from copy import deepcopy
from math import ceil, sqrt
from utils import Utils
from window_coord_controller import WindowCoordController
from obj_descriptor import OBJDescriptor

class World:
    def __init__(self) -> None:
        self.__object_list = []
        self.__viewport = [10,10,750,490]
        self.__window = WindowCoordController(
            p=(370,240),
            vup=(0,240),
            u=(370, 0)
        )
        # self.__window = [0,0,500,500]
        self.__zoom = 1

    def search_object_by_name(self, name: str):
        for obj in self.__object_list:
            if name == obj.get_name():
                return obj
        return None 

    def create_object(self, coord: tuple, color: str, name: str, obj_type, canvas) -> None:
        if self.search_object_by_name(name) != None:
            return 2

        new_object = obj_type(coord, color, name, "", canvas)
        if not new_object.valid:
            return 3
        self.__object_list.append(new_object)
        self.__window.add_obj(new_object.get_name(), new_object.get_coord())

        new_object.draw(self.__viewport, self.__window.get_coords()[name], self.__zoom)
        return 1
    
    def __find_object(self, name: str) -> int:

        for i, obj in enumerate(self.__object_list):

            if name == obj.get_name():

                return i
            
        return None

    def delete_object(self, name):

        obj_index = self.__find_object(name)

        if obj_index is not None:

            obj = self.__object_list[obj_index]
            obj.delete()
            self.__object_list.pop(obj_index)
            del obj

    def translate_object(self, name: str, dx: int, dy: int) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:

            obj = self.__object_list[obj_index]
            m = Utils.gen_translation_matrix(dx, dy)
            obj.transform(m)
            self.__window.att_obj(name, obj.get_coord())
            obj.draw(self.__viewport, self.__window.get_coords()[name], self.__zoom)

            return True

    def scale_object(self, name: str, sx: int, sy: int) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:

            obj = self.__object_list[obj_index]
            (cx, cy) = obj.get_center_coord()

            m = Utils.gen_scaling_matrix(
                sx=sx,
                sy=sy,
                cx=cx, 
                cy=cy
            )
            obj.transform(m)
            self.__window.att_obj(name, obj.get_coord())
            obj.draw(self.__viewport, self.__window.get_coords()[name], self.__zoom)

            return True
    
    def rotate_object(self, name: str, angle: float, arbitrary_point: tuple) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:

            obj = self.__object_list[obj_index]

            if arbitrary_point == None:
                (cx, cy) = obj.get_center_coord()
            else:
                (cx, cy) = arbitrary_point

            m = Utils.gen_rotation_matrix(
                angle=angle,
                cx=cx,
                cy=cy
            )
            obj.transform(m)
            self.__window.att_obj(name, obj.get_coord())
            obj.draw(self.__viewport, self.__window.get_coords()[name], self.__zoom)

            return True
    
    def move_window(self, dx, dy):

        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.move(dx, dy, objs)

        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window.get_coords()[obj.get_name()], self.__zoom)

    def zoom_window(self, pct):
        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.scale(pct, objs)
        # redraw canvas objects
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window.get_coords()[obj.get_name()], self.__zoom)

    def rotate_window(self, angle: float):
        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.rotate(angle, objs)
        # redraw canvas objects
        for obj in self.__object_list:
            obj.draw(self.__viewport, self.__window.get_coords()[obj.get_name()], self.__zoom)

    def save(self, filepath: str) -> bool:
        if len(self.__object_list) == 0:
            return False
        OBJDescriptor.obj_to_wavefront(self.__object_list[0], filepath, True)
        for obj in self.__object_list[1:]:
            OBJDescriptor.obj_to_wavefront(obj, filepath, False)
        return True
    
    def load(self, filepath: str, canvas) -> bool:

        # try:
            for object_ in self.__object_list:
                self.delete_object(object_)
            objs = OBJDescriptor.wavefront_to_obj(filepath, canvas)
            self.__object_list = objs

            names = list()
            for object_ in self.__object_list:

                self.__window.add_obj(object_.get_name(), object_.get_coord())
                names.append(object_.get_name())
                object_.draw(self.__viewport, self.__window.get_coords()[object_.get_name()], self.__zoom)

            return names
        # except Exception as e:
        #     print(e)
        #     return False