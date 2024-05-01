from canvas_object import CanvasObject
from wireframe2d import Wireframe2D
from polygon2d import Polygon2D
from point2d import Point2D
from line import Line
from bezier_curve import BezierCurve
from bspline_curve import BSplineCurve

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
    