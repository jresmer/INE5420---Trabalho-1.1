from window_gui import WindowGUI
import tkinter as tk
from tkinter.colorchooser import askcolor
from canvas_object_manager import CanvasObjectManager
from table_window import TableWindow


class ObjectCreationWindow(WindowGUI):

    def __init__(self, controller) -> None:
        self.__controller = controller
        
        self.__obj_man = CanvasObjectManager()
        self.__table_window = TableWindow(self)

        # create empty widget list
        self.__widgets = dict()

    def init_window(self) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("500x200") 

        self.init_widgets()  

        # TODO: deletar testes realizados depois
        # self.__controller.create_object(list(eval("(50,50,10)")), "blue", "Arroz", self.__obj_man.get_object_type("Point"))
        # self.__controller.create_object(list(eval("(0,0,0),(740,480,0)")), "green", "Feijão", self.__obj_man.get_object_type("Line"))
        # self.__controller.create_object(list(eval("(0,0,0),(0,5000,0)")), "green", "EixoY", self.__obj_man.get_object_type("Line"))
        # self.__controller.create_object(list(eval("(0,0,0),(5000,0,0)")), "green", "EixoX", self.__obj_man.get_object_type("Line"))
        # self.__controller.create_object(list(eval("(200,100,0),(100,500,0),(300,300,0)")), "red", "Carne", self.__obj_man.get_object_type("Polygon2D"))
        # self.__controller.create_object(list(eval("(100,100,0),(100,500,0),(400,300,0),(100,100,0)")), "pink", "Moida", self.__obj_man.get_object_type("Wireframe"))
        # self.__controller.create_object(list(eval("(420,200,0),(320,200,0),(370,300,0),(370,300,50),(420,200,50),(320,200,50),(320,200,0),(420,200,0),(420,200,50),(370,300,50),(370,300,0),(420,200,0)")), "red", "Prisma", self.__obj_man.get_object_type("Wireframe"))
        # self.__controller.create_object(list(eval("(0,0,0),(100,100,0),(100,500,0),(400,300,0)")), "dark blue", "Cabritinho", self.__obj_man.get_object_type("BezierCurve"))
        # self.__controller.create_object(list(eval("(0,0,0),(0,0,0),(100,100,0),(300,100,0),(500,300,0),(500,300,0)")), "dark blue", "Cabrio", self.__obj_man.get_object_type("BSplineCurve"))
        # coord = []
        # for i in range(16):
        #     if i < 12:
        #         line = [(0,0,i*10),(100,100,i*10),(100,500,i*10),(400,300,i*10)] + [(400,300,i*10),(600,100,i*10),(600,500,i*10),(900,300,i*10)] + [None]*8
        #     else:
        #         line = [None]*4 + [(400,300,i*10),(600,100,i*10),(600,500,i*10),(900,300,i*10)] + [None]*8
            
        #     # print(line)
        #     coord.append(line)

        # self.__controller.create_object(coord, "green", "EixoX", self.__obj_man.get_object_type("BezierSurface"))

        self.__root.mainloop()

    def att_coords_form(self, *args):
        if "coord txt box" in self.__widgets.keys():
            self.__widgets["coord txt box"].destroy()
        if "create table bt" in self.__widgets.keys():
            self.__widgets["create table bt"].destroy()
            self.__table_window.destroy()

        if self.__widgets["type choice box txt"].get() not in ["BezierSurface", "BSplineSurface"]:
            text_box = tk.Text(self.__root, height=1, width=40)
            text_box.place(x=100, y=35)
            self.__widgets["coord txt box"] = text_box
        else:   
            button = tk.Button(self.__root, text="Call table", command = self.create_table)
            button.place(x=100, y=35)
            self.__widgets["create table bt"] = button

    def get_coords(self):
        if self.__widgets["type choice box txt"].get() not in ["BezierSurface", "BSplineSurface"]:
            return list(eval(self.__widgets["coord txt box"].get("1.0", "end-1c")))
        else:
            return self.__table_window.get_table_values()

    def create_table(self):
        if self.__widgets["type choice box txt"].get() == "BezierSurface":
            self.__table_window.set_n(16)
        else:
            self.__table_window.set_n(20)
        self.__table_window.init_window()

    def select_color(self):
        color = askcolor(title="Object Color Selection")
        self.__widgets["selected color"].config(background = color[1])

    def create(self):

        name = self.__widgets["name txt box"].get("1.0", "end-1c")
        try:
            coords = self.get_coords()

            type_ = self.__widgets["type choice box txt"].get()
            tk_color = self.__widgets["selected color"].cget('background')
            
            obj_type = self.__obj_man.get_object_type(type_)
            
            if self.__controller.create_object(
                                                coords,
                                                tk_color,
                                                name,
                                                obj_type
                                            ):
            
                self.__root.destroy()
                self.__table_window.destroy()

        except Exception as e:
            self.__controller.notify_status("Coordenadas digitadas incorretamente. Reveja o formato e tipo utilizado")

    def init_widgets(self) -> None:

        button = tk.Button(self.__root, text="Create", command = self.create)
        button.place(x=185, y=150)
        self.__widgets["create bt"] = button

        button = tk.Button(self.__root, text="Cancel", command= self.__root.destroy)
        button.place(x=260, y=150)
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

        label = tk.Label(self.__root, text="(x1, y1, z1),(x2, y2, z2),...")
        label.place(x=100, y= 60)
        self.__widgets["coord form"] = label

        #Object type choice
        label = tk.Label(self.__root, text="Object type:")
        label.place(x=10, y= 110)
        self.__widgets["obj type lbl"] = label

        choices = self.__obj_man.get_all_object_types()
        var_str = tk.StringVar(self.__root)
        var_str.set("---")
        choice_box = tk.OptionMenu(self.__root, var_str, *choices)
        choice_box.place(x=100, y=105)
        self.__widgets["type choice box txt"] = var_str
        self.__widgets["type choice box"] = choice_box
        var_str.trace_add("write", self.att_coords_form)

        #Object color choice
        label = tk.Label(self.__root, text="Object color:")
        label.place(x=220, y= 110)
        self.__widgets["obj color lbl"] = label

        button = tk.Button(self.__root, text="Select Color", command= self.select_color)
        button.place(x=310, y=105)
        self.__widgets["color bt"] = button

        label = tk.Label(self.__root, background= "red", width=2)
        label.place(x=420, y=110)
        self.__widgets["selected color"] = label
