from window_gui import WindowGUI
import tkinter as tk


class ObjectCreationWindow(WindowGUI):

    def __init__(self, controller) -> None:
        self.__controller = controller
        

        # create empty wighet list
        self.__widget_list = list()

    def init_window(self, world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("500x100") 
        self.init_widgets(world)   
        self.__root.mainloop()

    # TODO - adicionar os widgets necessários + adicionar comandos aos botões
    def init_widgets(self, world) -> None:

        button = tk.Button(self.__root, text="Create", command= lambda: self.__controller.debug_print("Created"))
        button.place(x=185, y=70)
        self.__widget_list.append(button)

        button = tk.Button(self.__root, text="Cancel", command= self.__root.destroy)
        button.place(x=260, y=70)
        self.__widget_list.append(button)

        label = tk.Label(self.__root, text="Object name:")
        label.place(x=10, y=10)
        self.__widget_list.append(label)

        text_box = tk.Text(self.__root, height=1, width=40)
        text_box.place(x=100, y=10)
        self.__widget_list.append(text_box)
