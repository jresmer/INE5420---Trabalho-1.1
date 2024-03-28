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

        status = self.world.create_object(
            coord,
            color,
            name,
            obj_type,
            self.windows[MainWindow.__name__].get_canvas()
        )
        if status == 1:
            self.windows[MainWindow.__name__].add_to_listbox(name)
            self.notify_status(f"Objeto {name} criado com sucesso")
        elif status == 2:
            self.notify_status(f"Já existe um objeto com o nome {name}")

    def revolve_object(self, name: str, dx: int, dy: int):

        self.world.revolve_object(name, dx, dy)

    def notify_status(self, text: str):
        self.windows[MainWindow.__name__].notify_status(text)

    def delete_object(self, name: str):
        self.world.delete_object(name)
        self.notify_status(f"Objeto {name} deletado")

    def zoom_window(self, pct: float):

        self.world.zoom_window(pct)
        self.windows[MainWindow.__name__].notify_status(f"")
