from world import World
from color import Color
from object_creation_window import ObjectCreationWindow
from main_window import MainWindow

class GUI:
    def __init__(self):
        self.current_window = None
        self.windows = {}
        self.world = World()
    
    def start_program(self):
        self.windows[MainWindow.__name__] = MainWindow(self)
        self.windows[ObjectCreationWindow.__name__] = ObjectCreationWindow(self)
        self.current_window = self.windows[MainWindow.__name__]
        
        self.current_window.init_window(1)
        
    def open_creation_window(self):
        self.windows[ObjectCreationWindow.__name__] = ObjectCreationWindow(self)
        self.current_window = self.windows[ObjectCreationWindow.__name__]
        self.current_window.init_window(1)

    def move_canvas(self, dx, dy):
        self.world.move_window(dx, dy)

    def debug_print(self, text: str):
        print(text)
        
    def create_object(self, coord: tuple, color: Color, name: str, obj_type) -> None:

        self.world.create_object(
            coord,
            color,
            name,
            obj_type,
            self.windows[MainWindow.__name__].get_canvas()
        )

        self.windows[MainWindow.__name__].add_to_listbox(self.world.get_last_object_name())

    def delete_object(self, name: str):
        self.world.delete_object(name)

    def zoom_window(self, pct: float):

        self.world.zoom_window(pct)
