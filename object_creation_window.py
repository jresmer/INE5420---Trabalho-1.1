from window_gui import WindowGUI
import tkinter as tk
from canvas_object_manager import CanvasObjectManager


class ObjectCreationWindow(WindowGUI):

    def __init__(self, controller) -> None:
        self.__controller = controller
        
        self.__obj_man = CanvasObjectManager()

        # create empty widget list
        self.__widgets = dict()

    def init_window(self, world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("500x150") 

        self.init_widgets(world)  

        # TODO: deletar testes realizados depois
        self.__controller.create_object(list(eval("(50,50)")), "blue", "Arroz", self.__obj_man.get_object_type("Point"))
        self.__controller.create_object(list(eval("(100,100),(200,200)")), "green", "Feijão", self.__obj_man.get_object_type("Line"))
        self.__controller.create_object(list(eval("(200,100),(100,500),(300,300)")), "red", "Carne", self.__obj_man.get_object_type("Polygon"))

        self.__root.mainloop()

    def create(self):

        name = self.__widgets["name txt box"].get("1.0", "end-1c")
        try:
            coords = list(eval(self.__widgets["coord txt box"].get("1.0", "end-1c")))
    
            type_ = self.__widgets["type choice box txt"].get()
            obj_type = self.__obj_man.get_object_type(type_)
            
            self.__controller.create_object(
                coords,
                "red",
                name,
                obj_type
            )

            self.__root.destroy()

        except:
            self.__controller.notify_status("Coordenadas digitadas incorretamente. Reveja o formato e o tipo utilizado")

    def init_widgets(self, world) -> None:

        button = tk.Button(self.__root, text="Create", command= self.create)
        button.place(x=185, y=120)
        self.__widgets["create bt"] = button

        button = tk.Button(self.__root, text="Cancel", command= self.__root.destroy)
        button.place(x=260, y=120)
        self.__widgets["cancel bt"] = button

        label = tk.Label(self.__root, text="Object name:")
        label.place(x=10, y=10)
        self.__widgets["name lbl"] = label

        text_box = tk.Text(self.__root, height=1, width=40)
        text_box.place(x=100, y=10)
        self.__widgets["name txt box"] = text_box

        label = tk.Label(self.__root, text="Coordinates:")
        label.place(x=10, y= 35)
        self.__widgets["coord lbl"] = label

        text_box = tk.Text(self.__root, height=1, width=40)
        text_box.place(x=100, y=35)
        self.__widgets["coord txt box"] = text_box

        label = tk.Label(self.__root, text="(x1, y1),(x2, y2),...")
        label.place(x=100, y= 60)
        self.__widgets["coord form"] = label

        label = tk.Label(self.__root, text="Object type:")
        label.place(x=10, y= 95)
        self.__widgets["coord lbl"] = label

        choices = self.__obj_man.get_all_object_types()
        var_str = tk.StringVar(self.__root)
        var_str.set("---")
        choice_box = tk.OptionMenu(self.__root, var_str, *choices)
        choice_box.place(x=100, y=90)
        self.__widgets["type choice box txt"] = var_str
        self.__widgets["type choice box"] = choice_box
