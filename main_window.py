import tkinter as tk
from window_gui import WindowGUI
from moveCanvas import MoveCanvas


class MainWindow(WindowGUI):

    DRAWING = True
    STANDARD = False

    def __init__(self, controller) -> None:
        self.__controller = controller
        # set initial state
        
        self.__state = self.STANDARD

        # create empty wighet list
        self.__widget_list = list()

    def init_window(self,world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("1280x900")
        self.init_widgets(world)

        #BIND PARA MOVER O CANVAS
        self.__root.bind("<KeyPress-Left>", lambda _: self.__widget_list[0].change_heading(-1, 0))
        self.__root.bind("<KeyPress-Right>", lambda _: self.__widget_list[0].change_heading(1, 0))
        self.__root.bind("<KeyPress-Up>", lambda _: self.__widget_list[0].change_heading(0, -1))
        self.__root.bind("<KeyPress-Down>", lambda _: self.__widget_list[0].change_heading(0, 1))

        self.__root.mainloop()
    
    # TODO - adicionar os widgets necessários + adicionar comandos aos botões
    def init_widgets(self, world) -> None:
        
        #canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")

        #TESTES PRO MOVIMENTO DO CANVAS
        canvas = MoveCanvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")

        canvas.add_object(canvas.create_line(50,50,30,30,10,20,50,50))
        canvas.add_object(canvas.create_line(100,100,300,300,100,200,100,100))
        canvas.add_object(canvas.create_line(700,700,300,300,100,200,500,500))
        #FIM DA PARTE DE TESTES

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
