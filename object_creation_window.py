from window_gui import WindowGUI
import tkinter as tk


class ObjectCreationWindow(WindowGUI):

    def __init__(self, controller) -> None:
        self.__controller = controller
        

        # create empty wighet list
        self.__widgets = dict()

    def init_window(self, world) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Sistema Gráfico")
        self.__root.geometry("500x150") 
        self.init_widgets(world)   
        self.__root.mainloop()

    # TODO - implementar função
    def create(self):

        self.__controller.debuh_print()

    # TODO - adicionar os widgets necessários + adicionar comandos aos botões
    def init_widgets(self, world) -> None:

        button = tk.Button(self.__root, text="Create", command= lambda: self.create())
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

        label = tk.Label(self.__root, text="Object type:")
        label.place(x=10, y= 65)
        self.__widgets["coord lbl"] = label

        # TODO - criar gerenciamento dos tipos disponíveis e acessar lista correta de opções
        choices = ["test-1", "test-2", "test-3"]
        var_str = tk.StringVar(self.__root)
        var_str.set("---")
        choice_box = tk.OptionMenu(self.__root, var_str, *choices)
        choice_box.place(x=100, y=60)
