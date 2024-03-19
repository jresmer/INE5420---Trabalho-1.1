from world import World
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
        
        