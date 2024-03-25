import tkinter as tk
from window_gui import WindowGUI


class MainWindow(WindowGUI):

    def __init__(self, controller) -> None:
        self.__controller = controller
        # set initial state

        # create empty wighet list
        self.__widgets = dict()

    def add_to_listbox(self, name):
        self.__widgets['list obj'].insert(tk.END,name)

    def get_canvas(self):
        return self.__widgets['canvas']

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
        self.__root.bind("<Button-4>", lambda _: self.on_mousewheel(-1))
        self.__root.bind("<Button-5>", lambda _: self.on_mousewheel(1))

        self.__root.mainloop()

    def on_mousewheel(self, multiplier: int):
        try:
            pct = int(self.__widgets["zoom txt box"].get("1.0", "end-1c"))
            multiplier *= pct/100
            self.__controller.zoom_window(pct=multiplier)
        except Exception as e:
            print(e)
            self.notify_status("Erro ao utilizar o zoom. Apenas valores inteiros aceitos no Step")

    def delete_object(self):
        active_obj_name = str(self.__widgets['list obj'].get(tk.ACTIVE))
        self.__controller.delete_object(active_obj_name)
        self.__widgets['list obj'].delete(tk.ACTIVE)

    def notify_status(self, text: str):
        self.__widgets['error msg box'].config(text=text)

    def init_widgets(self, world) -> None:
        
        canvas = tk.Canvas(master=self.__root, height=500, width=760, bd=3, relief="ridge")
        canvas.place(x=500, y=0)
        self.__widgets['canvas'] = canvas

        text = "Status messages will appear here!\n"
        error_message_box = tk.Label(self.__root, height=18, width=84, 
                                     bd=3, relief="ridge", text=text, justify="left")
        error_message_box.place(x=500, y=550)
        self.__widgets['error msg box'] = error_message_box

        self.init_operations_object()

        self.init_operations_window()
    
    def init_operations_object(self):

        button = tk.Button(self.__root, text="Create Object", command= lambda: self.__controller.open_creation_window())
        button.place(x=0, y=235)
        self.__widgets['create obj button'] = button

        button = tk.Button(self.__root, text="Delete Selected Object", 
                            command= lambda: self.delete_object())
        button.place(x=0, y=205)
        self.__widgets['delete obj button'] = button

        list_objects = tk.Listbox(self.__root, width= 21)
        list_objects.place(x = 0, y = 20)
        self.__widgets['list obj'] = list_objects

        title = tk.Label(self.__root, text="Objects List", justify="left")
        title.place(x = 0, y = 0)
        self.__widgets['title list obj'] = title

    def init_operations_window(self):
        
        frame = tk.Frame(self.__root, height = 200, width = 250, relief="ridge", borderwidth=2)
        frame.place(x=200, y = 5)

        label = tk.Label(frame, text = "Window Operations")
        label.place(x=0, y = 0)
        self.__widgets["title ops window lbl"] = label

        button = tk.Button(frame, text="Zoom in",
                           command= lambda: self.on_mousewheel(1))
        button.place(x=10, y=35)
        self.__widgets['zoom in button'] = button

        button = tk.Button(frame, text="Zoom out", 
                           command= lambda: self.on_mousewheel(-1))
        button.place(x=5, y=65)
        self.__widgets['zoom out button'] = button

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=140, y=50)
        self.__widgets["zoom txt box"] = text_box

        label = tk.Label(frame, text = "%")
        label.place(x=180, y=50)
        self.__widgets["percent zoom lbl"] = label

        label = tk.Label(frame, text = "Step")
        label.place(x=100, y=50)
        self.__widgets["zoom lbl"] = label

        button = tk.Button(frame, text="↑", width= 2,  
                           command= lambda : self.__controller.move_canvas(0, -3))
        button.place(x=100, y=110)
        self.__widgets['move window up button'] = button

        button = tk.Button(frame, text="↓", width= 2, 
                           command= lambda : self.__controller.move_canvas(0, 3))
        button.place(x=100, y=140)
        self.__widgets['move window down button'] = button

        button = tk.Button(frame, text="←", width= 2, 
                           command= lambda : self.__controller.move_canvas(-3, 0))
        button.place(x=55, y=125)
        self.__widgets['move window left button'] = button

        button = tk.Button(frame, text="→", width= 2, 
                           command= lambda : self.__controller.move_canvas(3, 0))
        button.place(x=145, y=125)
        self.__widgets['move window right button'] = button
