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
            p=(370,240,0),
            vup=(0,240,0),
            u=(370, 0,0),
            vpn=(0, 0, 370)
        )
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
        window_coords = self.__window.get_coords()

        if len(window_coords[name]) > 0:
            new_object.draw(self.__viewport, window_coords[name], self.__zoom)

        return 1
    
    def __find_object(self, name: str) -> int:

        for i, obj in enumerate(self.__object_list):

            if name == obj.get_name():

                return i
            
        return None
    
    def __draw_all(self):

        window_coords = self.__window.get_coords()
        # redraw canvas objects
        for obj in self.__object_list:

            obj_window_coords = window_coords[obj.get_name()]
            if len(obj_window_coords) > 0:
                obj.delete()
                obj.draw(self.__viewport, obj_window_coords, self.__zoom)

    def delete_object(self, name):

        obj_index = self.__find_object(name)

        if obj_index is not None:

            obj = self.__object_list[obj_index]
            obj.delete()
            self.__object_list.pop(obj_index)
            del obj

    def translate_object(self, name: str, dx: int, dy: int, dz: int) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:

            obj = self.__object_list[obj_index]
            m = Utils.gen_3d_translation_matrix(dx, dy, dz)
            obj.transform(m)
            self.__window.att_obj(name, obj.get_coord())
            window_coords = self.__window.get_coords()
            obj.delete()
            if len(window_coords[name]) > 0:
                obj.draw(self.__viewport, window_coords[name], self.__zoom)

            return True

    def scale_object(self, name: str, sx: int, sy: int, sz: int) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:
            
            obj = self.__object_list[obj_index]
            (cx,cy,cz) = obj.get_center_coord()

            m = Utils.gen_3d_scaling_matrix(
                sx=sx, sy=sy, sz=sz,
                cx=cx, cy=cy, cz=cz
            )
            obj.transform(m)
            self.__window.att_obj(name, obj.get_coord())
            window_coords = self.__window.get_coords()
            obj.delete()
            if len(window_coords[name]) > 0:
                obj.draw(self.__viewport, window_coords[name], self.__zoom)

            return True
    
    def rotate_object(self, name: str, axis: str, angle: float, arb_axis: tuple, arb_point) -> bool:

        obj_index = self.__find_object(name)

        if obj_index is None:

            return False
        
        else:
            obj = self.__object_list[obj_index]

            if not arb_point:
                p = obj.get_center_coord()
            else:
                p = arb_point

            if axis == "x":
                a = (1,0,0)
            elif axis == "y":
                a = (0,1,0)
            elif axis == "z":
                a = (0,0,1)
            elif axis == "object axis":
                a = obj.get_obj_axis()
            else:
                a = arb_axis

            m = Utils.gen_3d_rotation_matrix(
                angle=angle, rotation_axis= ((p,a))
            )
            obj.transform(m)

            if axis != "object axis":
                obj.att_obj_axis(m)

            self.__window.att_obj(name, obj.get_coord())
            window_coords = self.__window.get_coords()
            obj.delete()
            if len(window_coords[name]) > 0:
                obj.draw(self.__viewport, window_coords[name], self.__zoom)

            return True
    
    def move_window(self, dx, dy,dz):
        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.move(dx, dy,dz, objs)
        self.__draw_all()

    def zoom_window(self, pct):
        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.scale(pct, objs)
        self.__draw_all()

    def rotate_window(self, axis, angle: float):
        objs = {obj.get_name(): obj.get_coord() for obj in self.__object_list}
        self.__window.rotate(axis, angle, objs)
        self.__draw_all()

    def save(self, filepath: str) -> bool:
        if len(self.__object_list) == 0:
            return False
        OBJDescriptor.obj_to_wavefront(self.__object_list[0], filepath, True)
        for obj in self.__object_list[1:]:
            OBJDescriptor.obj_to_wavefront(obj, filepath, False)
        return True
    
    def load(self, filepath: str, canvas) -> bool:
        try:
            for object_ in self.__object_list:
                self.delete_object(object_)
            objs = OBJDescriptor.wavefront_to_obj(filepath, canvas)
            self.__object_list = objs
            window_coords = self.__window.get_coords()
            names = list()
            for object_ in self.__object_list:

                self.__window.add_obj(object_.get_name(), object_.get_coord())
                names.append(object_.get_name())
                object_.draw(self.__viewport, window_coords[object_.get_name()], self.__zoom)

            return names
        except:
            return None
