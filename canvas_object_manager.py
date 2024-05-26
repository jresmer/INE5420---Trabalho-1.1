from canvas_object import CanvasObject
from wireframe import Wireframe
from polygon2d import Polygon2D
from point import Point
from line import Line
from bezier_curve import BezierCurve
from bspline_curve import BSplineCurve
from bezier_surface import BezierSurface
from bspline_surface import BSplineSurface

class CanvasObjectManager:

    def __init__(self):

        subclasses = list(CanvasObject.__subclasses__())
        self.__objects = {subclass.__name__ : subclass for subclass in subclasses}

    def get_object_type(self, name: str):

        if name in self.__objects:

            return self.__objects[name]
        
        return None
    
    def get_all_object_types(self):

        return [object_type for object_type in self.__objects]
    