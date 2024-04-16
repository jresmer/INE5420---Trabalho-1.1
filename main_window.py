import tkinter as tk
from tkinter import filedialog
from window_gui import WindowGUI
from utils import Clipping

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
        self.__root.bind("<KeyPress-Up>", lambda _: self.__controller.move_canvas(0, 3))
        self.__root.bind("<KeyPress-Down>", lambda _: self.__controller.move_canvas(0, -3))
        self.__root.bind("<Button-4>", lambda _: self.on_mousewheel(-1))
        self.__root.bind("<Button-5>", lambda _: self.on_mousewheel(1))

        self.__root.mainloop()

    def on_mousewheel(self, multiplier: int):
        try:
            pct = int(self.__widgets["zoom txt box"].get("1.0", "end-1c"))
            multiplier *= pct/100
            self.__controller.zoom_window(pct=multiplier)
        except Exception as e:
            self.notify_status("Value error for zoom functionality - value should be an integer")

    def save_file(self):
        try:
            filepath = filedialog.asksaveasfilename(initialfile= "wavefront", defaultextension=".obj", initialdir = "/",
                                                        title = "Saving world")
            self.__controller.save_world(filepath)
        except:
            self.notify_status(f"World not saved. It doesn't have objects to save or save canceled by user")

    def load_file(self):
        try:
            filepath = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select wavefront .obj file")
            self.__controller.load_world(filepath)
        except:
            self.notify_status(f"World not loaded")

    def translate(self):
        try:
            self.__controller.translate_object(
                name=self.__widgets["list obj"].get(tk.ACTIVE),
                dx=int(self.__widgets["move dx obj txt box"].get("1.0", "end-1c")),
                dy=int(self.__widgets["move dy obj txt box"].get("1.0", "end-1c"))
            )
        except ValueError as e:
            self.notify_status("Error: the value to dx and dy has to be an integer number")
    
    def scaletion(self, up: bool):
        try:
            if up:
                self.__controller.scale_object(
                    name=self.__widgets["list obj"].get(tk.ACTIVE),
                    sx=float(self.__widgets["scale txt box"].get("1.0", "end-1c")),
                    sy=float(self.__widgets["scale txt box"].get("1.0", "end-1c"))
                )
            else:
                self.__controller.scale_object(
                    name=self.__widgets["list obj"].get(tk.ACTIVE),
                    sx=1/float(self.__widgets["scale txt box"].get("1.0", "end-1c")),
                    sy=1/float(self.__widgets["scale txt box"].get("1.0", "end-1c"))
                )
        except ValueError as e:
            self.notify_status("Error: the value to scale has to be a float")

    def rotate_window(self, direction: int):
        try:
            self.__controller.rotate_window(
                angle=direction*float(self.__widgets["rotate window txt box"].get("1.0", "end-1c"))
            )
        except ValueError as e:
            self.notify_status("Error: the value to rotate has to be a float (in degrees)")

    def rotation(self, direction: int):

        try:   
            mode = self.__widgets["rotate obj mode choice box txt"].get()
            if mode == "Object Center":
                self.__controller.rotate_object(
                    name=self.__widgets["list obj"].get(tk.ACTIVE),
                    angle=direction*float(self.__widgets["rotate obj txt box"].get("1.0", "end-1c")),
                    arbitrary = None
                )
            elif mode == "World Origin":
                self.__controller.rotate_object(
                    name=self.__widgets["list obj"].get(tk.ACTIVE),
                    angle=direction*float(self.__widgets["rotate obj txt box"].get("1.0", "end-1c")),
                    arbitrary = (0,0)
                )
            else:
                x = int(self.__widgets["rotate arbitrary x obj txt box"].get("1.0", "end-1c"))
                y = int(self.__widgets["rotate arbitrary y obj txt box"].get("1.0", "end-1c"))
                self.__controller.rotate_object(
                    name=self.__widgets["list obj"].get(tk.ACTIVE),
                    angle=direction*float(self.__widgets["rotate obj txt box"].get("1.0", "end-1c")),
                    arbitrary = (x,y)
                )
        except ValueError as e:
            self.notify_status("Error: the value to rotate has to be a float (in degrees) and\nfor arbitrary point x,y has to be integers")

    def delete_object(self):
        active_obj_name = str(self.__widgets['list obj'].get(tk.ACTIVE))
        self.__controller.delete_object(active_obj_name)
        self.__widgets['list obj'].delete(tk.ACTIVE)

    def notify_status(self, text: str):
        self.__widgets['error msg box'].config(text=text)

    def init_widgets(self, world) -> None:
        
        canvas = tk.Canvas(master=self.__root, height=500, width=760, bg="white",relief="ridge")
        canvas.create_line(10,10,10,490)
        canvas.create_line(10,490,750,490)
        canvas.create_line(750,490,750,10)
        canvas.create_line(750,10,10,10)
        canvas.place(x=500, y=0)
        self.__widgets['canvas'] = canvas

        text = "Status messages will appear here!\n"
        error_message_box = tk.Label(self.__root, height=18, width=84, 
                                     bd=3, relief="ridge", text=text, justify="left")
        error_message_box.place(x=500, y=550)
        self.__widgets['error msg box'] = error_message_box

        self.init_list_object()

        self.init_operations_window()

        self.init_operations_object()

        self.init_operations_world()

        self.init_change_clipping()
    
    def init_list_object(self):

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

        #Zoom part
        button = tk.Button(frame, text="In",
                           command= lambda: self.on_mousewheel(1))
        button.place(x=180, y=35)
        self.__widgets['zoom in button'] = button

        button = tk.Button(frame, text="Out", 
                           command= lambda: self.on_mousewheel(-1))
        button.place(x=65, y=35)
        self.__widgets['zoom out button'] = button

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=120, y=35)
        self.__widgets["zoom txt box"] = text_box

        label = tk.Label(frame, text = "%")
        label.place(x=160, y=35)
        self.__widgets["percent zoom lbl"] = label

        label = tk.Label(frame, text = "Zoom\nStep")
        label.place(x=7, y=30)
        self.__widgets["zoom lbl"] = label

        #Rotate Window Part
        button = tk.Button(frame, text="⟳",
                           command= lambda: self.rotate_window(1))
        button.place(x=180, y=75)
        self.__widgets['rotate window right button'] = button

        button = tk.Button(frame, text="⟲", 
                           command= lambda: self.rotate_window(-1))
        button.place(x=70, y=75)
        self.__widgets['rotate window left button'] = button

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=120, y=75)
        self.__widgets["rotate window txt box"] = text_box

        label = tk.Label(frame, text = "º")
        label.place(x=160, y=75)
        self.__widgets["degreee window simbol lbl"] = label

        label = tk.Label(frame, text = "Rotate")
        label.place(x=5, y=80)
        self.__widgets["rotate window lbl"] = label


        #Move Window Part
        button = tk.Button(frame, text="↑", width= 2,  
                           command= lambda : self.__controller.move_canvas(0, 3))
        button.place(x=100, y=120)
        self.__widgets['move window up button'] = button

        button = tk.Button(frame, text="↓", width= 2, 
                           command= lambda : self.__controller.move_canvas(0, -3))
        button.place(x=100, y=150)
        self.__widgets['move window down button'] = button

        button = tk.Button(frame, text="←", width= 2, 
                           command= lambda : self.__controller.move_canvas(-3, 0))
        button.place(x=55, y=135)
        self.__widgets['move window left button'] = button

        button = tk.Button(frame, text="→", width= 2, 
                           command= lambda : self.__controller.move_canvas(3, 0))
        button.place(x=145, y=135)
        self.__widgets['move window right button'] = button

    def init_operations_object(self):
                
        frame = tk.Frame(self.__root, height = 270, width = 250, relief="ridge", borderwidth=2)
        frame.place(x=200, y = 220)

        label = tk.Label(frame, text = "Selected Object Operations")
        label.place(x=0, y = 0)
        self.__widgets["title ops obj lbl"] = label

    #Rotate Part

        label = tk.Label(frame, text="Rotate")
        label.place(x=0, y= 30)
        self.__widgets["rotate obj mode lbl"] = label
    
        label = tk.Label(frame, text="Mode:")
        label.place(x=20, y= 50)

        choices = ["Object Center", "World Origin", "Arbitrary Point"]
        var_str = tk.StringVar(frame)
        var_str.set("Object Center")
        choice_box = tk.OptionMenu(frame, var_str, *choices)
        choice_box.place(x=60, y=45)
        self.__widgets["rotate obj mode choice box txt"] = var_str
        self.__widgets["rotate obj mode choice box"] = choice_box

        button = tk.Button(frame, text="✓",
                           command= lambda: self.att_rotate_mode_object())
        button.place(x=200, y=45)

        rotate_frame = tk.Frame(frame, height = 70, width = 240, relief="ridge")
        self.__widgets["rotate obj frame"] = rotate_frame
        rotate_frame.place(x=0, y = 85)

        self.att_rotate_mode_object()


    #Scale part
        button = tk.Button(frame, text="+",
                           command= lambda: self.scaletion(True))
        button.place(x=180, y=175)
        self.__widgets['scale up button'] = button

        button = tk.Button(frame, text="--", 
                           command= lambda: self.scaletion(False))
        button.place(x=70, y=175)
        self.__widgets['scale down button'] = button

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=120, y=175)
        self.__widgets["scale txt box"] = text_box

        label = tk.Label(frame, text = "x")
        label.place(x=160, y=175)
        self.__widgets["x simbol lbl"] = label

        label = tk.Label(frame, text = "Scale")
        label.place(x=5, y=180)
        self.__widgets["scale obj lbl"] = label
    
    #Move part

        #dx
        label = tk.Label(frame, text = "dx")
        label.place(x=60, y=220)
        self.__widgets["move dx obj lbl"] = label

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=80, y=220)
        self.__widgets["move dx obj txt box"] = text_box

        #dy
        label = tk.Label(frame, text = "dy")
        label.place(x=120, y=220)
        self.__widgets["move dy obj lbl"] = label

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=140, y=220)
        self.__widgets["move dy obj txt box"] = text_box

        button = tk.Button(frame, text = "✓", command = lambda: self.translate())
        button.place(x=180, y=215)
        self.__widgets["move obj button"] = button

        label = tk.Label(frame, text = "Move")
        label.place(x=5, y=220)
        self.__widgets["move obj lbl"] = label

    def att_rotate_mode_object(self):
        frame = self.__widgets["rotate obj frame"]

        text_box = tk.Text(frame, height=1, width=4)
        text_box.place(x=120, y=0)
        self.__widgets["rotate obj txt box"] = text_box

        label = tk.Label(frame, text = "º")
        label.place(x=160, y=0)

        button = tk.Button(frame, text="⟳",
                           command= lambda: self.rotation(1))
        button.place(x=180, y=0)
        self.__widgets['rotate obj right button'] = button

        button = tk.Button(frame, text="⟲", 
                           command= lambda: self.rotation(-1))
        button.place(x=70, y=0)
        self.__widgets['rotate obj left button'] = button

        mode = self.__widgets["rotate obj mode choice box txt"].get()

        if mode == "Arbitrary Point":
            #x
            label = tk.Label(frame, text = "x")
            label.place(x=70, y=40)

            text_box = tk.Text(frame, height=1, width=4)
            text_box.place(x=90, y=40)
            self.__widgets["rotate arbitrary x obj txt box"] = text_box

            #y
            label = tk.Label(frame, text = "y")
            label.place(x=130, y=40)

            text_box = tk.Text(frame, height=1, width=4)
            text_box.place(x=150, y=40)
            self.__widgets["rotate arbitrary y obj txt box"] = text_box

    def init_operations_world(self):
        frame = tk.Frame(self.__root, height = 100, width = 250, relief="ridge", borderwidth=2)
        frame.place(x=200, y = 505)

        label = tk.Label(frame, text = "World Operations")
        label.place(x=0, y = 0)
        self.__widgets["title ops window lbl"] = label

        button = tk.Button(frame, text="Load World", 
                           command= lambda: self.load_file())
        button.place(x=130, y=35)
        self.__widgets['rotate obj left button'] = button

        button = tk.Button(frame, text="Save World",
                           command= lambda: self.save_file())
        button.place(x=10, y=35)
        self.__widgets['rotate obj right button'] = button

    def change_clipping(self):
        v = self.__widgets["var line clipping"]
        Clipping.instance().change_line_clipping(v.get())
        self.__controller.move_canvas(0,0)

    def init_change_clipping(self):
        clippings = Clipping.instance().get_all_line_clippings()
        

        frame = tk.Frame(self.__root, height = 100, width = 150, relief="ridge", borderwidth=2)
        frame.place(x=10, y=300)

        label = tk.Label(frame, text = "Line Clipping")
        label.place(x=0, y = 0)


        v = tk.StringVar(frame, "1")
        self.__widgets["var line clipping"] = v
        (x,y) = 15,25
        for (text, value) in clippings.items(): 
            tk.Radiobutton(master = frame, text = text, variable = v, indicatoron=0,
                value = value, command=lambda: self.change_clipping()).place(x=x,y=y)
            y += 25
            

