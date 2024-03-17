from main_window import MainWindow
from object_creation_window import ObjectCreationWindow


if __name__ == "__main__":

    main_window = ObjectCreationWindow()
    main_window.init_widgets(1)
    main_window.init_window()
