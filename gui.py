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
            

    def move_window(self, dx, dy,dz):
        self.world.move_window(dx, dy,dz)
        self.notify_status("Window successfully moved")

    def create_object(self, coord: tuple, color: str, name: str, obj_type) -> None:

        status = self.world.create_object(
            coord,
            color,
            name,
            obj_type,
            self.windows[MainWindow.__name__].get_canvas()
        )
        if status == 1:
            self.windows[MainWindow.__name__].add_to_listbox(name)
            self.notify_status(f"Object name: {name} successfully created")
        elif status == 2:
            self.notify_status(f"Name: {name} is already assigned")
        elif status == 3:
            self.notify_status(f"Input coordinates don't satisfy constricts to object creation")

    def translate_object(self, name: str, dx: int, dy: int, dz: int):

        success = self.world.translate_object(name, dx, dy, dz)

        if success:

            self.notify_status("Successfull transformation applied to object {}".format(name))

        else:

            self.notify_status("Unsucessfull transformation")

    def scale_object(self, name: str, sx: int, sy: int, sz: int):

        success = self.world.scale_object(name, sx, sy, sz)

        if success:

            self.notify_status("Successfull transformation applied to object {}".format(name))

        else:

            self.notify_status("Unsucessfull transformation")

    def rotate_object(self, name: str, axis: str, angle: float, arb_axis: tuple, arb_point):

        success = self.world.rotate_object(name, axis, angle, arb_axis, arb_point)

        if success:

            self.notify_status("Successfull transformation applied to object {}".format(name))

        else:

            self.notify_status("Unsucessfull transformation")

    def notify_status(self, text: str):
        self.windows[MainWindow.__name__].notify_status(text)

    def delete_object(self, name: str):
        self.world.delete_object(name)
        self.notify_status(f"Object name: {name} deleted")

    def rotate_window(self, axis, angle: float):
        self.world.rotate_window(axis, angle)
        self.windows[MainWindow.__name__].notify_status(f"Window successfully rotated")

    def zoom_window(self, pct: float):
        self.world.zoom_window(pct)
        self.windows[MainWindow.__name__].notify_status(f"Window successfully zommed")

    def save_world(self, filepath: str):
        if self.world.save(filepath):
            self.notify_status(f"World saved on {filepath}")
        else:
            self.notify_status(f"World not saved. It doesn't have objects to save or save canceled by user")

    def load_world(self, filepath: str):
        names = self.world.load(filepath, self.windows[MainWindow.__name__].get_canvas())
        if names:
            self.notify_status(f"World {filepath} loaded")
            for name in names:
                self.windows[MainWindow.__name__].add_to_listbox(name)
        else:
            self.notify_status(f"World not loaded")
