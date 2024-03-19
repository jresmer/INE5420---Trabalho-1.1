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
        self.__widget_list = list()

    def get_canvas(self):
        return self.__widget_list[0]

    def init_window(self,world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("1280x900")
        self.init_widgets(world)

        #TESTE, APAGAR DEPOIS
        self.__controller.world.create_point((50,50),self.__controller.windows[MainWindow.__name__].get_canvas(), )

        #BIND PARA MOVER O CANVAS
        self.__root.bind("<KeyPress-Left>", lambda _: self.__controller.move_canvas(1, 0))
        self.__root.bind("<KeyPress-Right>", lambda _: self.__controller.move_canvas(-1, 0))
        self.__root.bind("<KeyPress-Up>", lambda _: self.__controller.move_canvas(0, 1))
        self.__root.bind("<KeyPress-Down>", lambda _: self.__controller.move_canvas(0, -1))

        self.__root.mainloop()
    
    # TODO - adicionar os widgets necessários + adicionar comandos aos botões
    def init_widgets(self, world) -> None:
        
        #canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")

        #TESTES PRO MOVIMENTO DO CANVAS
        canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")


        canvas.place(x=500, y=0)
        self.__widget_list.append(canvas)

        button = tk.Button(self.__root, text="Create Object", command= lambda: self.__controller.open_creation_window())
        button.place(x=0, y=0)
        self.__widget_list.append(button)

        text = "Status messages will appear here!\n"
        error_message_box = tk.Label(self.__root, height=18, width=84, 
                                     bd=3, relief="ridge", text=text, justify="left")
        error_message_box.place(x=500, y=550)
        self.__widget_list.append(error_message_box)
