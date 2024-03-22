import tkinter as tk
from window_gui import WindowGUI


class MainWindow(WindowGUI):

    DRAWING = True
    STANDARD = False

    def __init__(self, controller) -> None:
        self.__controller = controller
        # set initial state
        
        self.__state = self.STANDARD

        # create empty wighet list
        self.__widget_list = dict()

    def add_to_listbox(self, name):
        self.__widget_list['list obj'].insert(tk.END,name)

    def get_canvas(self):
        return self.__widget_list['canvas']

    def init_window(self,world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("1280x900")
        self.init_widgets(world)

        #BIND PARA MOVER O CANVAS
        self.__root.bind("<KeyPress-Left>", lambda _: self.__controller.move_canvas(-3, 0))
        self.__root.bind("<KeyPress-Right>", lambda _: self.__controller.move_canvas(3, 0))
        self.__root.bind("<KeyPress-Up>", lambda _: self.__controller.move_canvas(0, -3))
        self.__root.bind("<KeyPress-Down>", lambda _: self.__controller.move_canvas(0, 3))
        self.__root.bind("<Button-4>", lambda _: self.on_mousewheel(1))
        self.__root.bind("<Button-5>", lambda _: self.on_mousewheel(-1))

        self.__root.mainloop()

    def on_mousewheel(self, multiplier: int):

        self.__controller.zoom_window(
            pct_x=0.02 * multiplier,
            pct_y=0.02 * multiplier
        )

    def delete_object(self):
        active_obj_name = str(self.__widget_list['list obj'].get(tk.ACTIVE))
        self.__controller.delete_object(active_obj_name)
        self.__widget_list['list obj'].delete(tk.ACTIVE)
    
    # TODO - adicionar os widgets necessários + adicionar comandos aos botões
    def init_widgets(self, world) -> None:
        
        #canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")

        #TESTES PRO MOVIMENTO DO CANVAS
        canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")

        canvas.place(x=500, y=0)
        self.__widget_list['canvas'] = canvas

        button = tk.Button(self.__root, text="Create Object", command= lambda: self.__controller.open_creation_window())
        button.place(x=0, y=0)
        self.__widget_list['create obj button'] = button

        button = tk.Button(self.__root, text="Delete Selected Object", 
                           command= lambda: self.delete_object())
        button.place(x=100, y=300)
        self.__widget_list['delete obj button'] = button

        list_objects = tk.Listbox(self.__root,)
        list_objects.place(x = 100, y = 100)
        self.__widget_list['list obj'] = list_objects

        text = "Status messages will appear here!\n"
        error_message_box = tk.Label(self.__root, height=18, width=84, 
                                     bd=3, relief="ridge", text=text, justify="left")
        error_message_box.place(x=500, y=550)
        self.__widget_list['error msg box'] = error_message_box
