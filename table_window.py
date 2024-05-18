from window_gui import WindowGUI
import tkinter as tk

class TableWindow(WindowGUI):
    def __init__(self, controller) -> None:
        self.__controller = controller

        # create empty widget list
        self.__widgets = dict()
        self.__n = 16
    
    def get_table_values(self):
        matrix = []
        for i in range(self.__n):
            matrix.append([None]*self.__n)
            for j in range(self.__n):
                matrix[i][j] = self.__widgets["matrix coords"][i][j].get()

        print(matrix)

    def set_n(self, new_n):
        self.__n = new_n

    def init_window(self) -> None:
        # instanciate Tk object and set the window's title and geometry
        self.__root = tk.Tk()
        self.__root.title("Tabela de valores")
        self.__root.geometry(f"{130*self.__n}x{20*self.__n}") 

        self.init_widgets()  

        self.__root.mainloop()

    def init_widgets(self):
        frame_table = tk.Frame(self.__root)
        
        self.__widgets["matrix coords"] = []
        for i in range(self.__n):
            self.__widgets["matrix coords"].append([None]*self.__n)
            for j in range(self.__n):
                e_value = tk.StringVar(frame_table)
                e = tk.Entry(frame_table, textvariable= e_value, width=12, font=('Arial', 9))
                self.__widgets["matrix coords"][i][j] = e_value
                e.grid(row=i, column=j)
                e.insert(tk.END, "")
        frame_table.pack()