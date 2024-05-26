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
                try:
                    matrix[i][j] = eval(self.__widgets["matrix coords"][i][j].get())
                except Exception as e:
                    pass
        # print(matrix)
        return matrix

    def destroy(self):
        try:
            self.__root.destroy()
        except:
            return

    def set_n(self, new_n):
        self.__n = new_n

    def init_window(self) -> None:
        # instanciate Tk object and set the window's title
        self.__root = tk.Tk()
        self.__root.title("Table Coords")

        self.init_widgets()  

        self.__root.mainloop()

    def init_widgets(self):

        master_frame = tk.Frame(self.__root, relief=tk.RIDGE)        
        master_frame.grid(sticky=tk.NSEW)        
        master_frame.columnconfigure(0, weight=1)        
      
        # Create a frame for the canvas and scrollbar(s).        
        frame2 = tk.Frame(master_frame)        
        frame2.grid(row=0, column=0, sticky=tk.NW)        
        # Add a canvas in that frame.        
        canvas = tk.Canvas(frame2)        
        canvas.grid(row=0, column=0, pady=5, padx=5)        
 
        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)        
        hsbar.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)        
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the buttons.        
        table_frame = tk.Frame(canvas)        
        # Add the buttons to the frame.        
        self.__widgets["matrix coords"] = []
        for i in range(self.__n):
            self.__widgets["matrix coords"].append([None]*self.__n)
            for j in range(self.__n):
                e_value = tk.StringVar(table_frame)
                e = tk.Entry(table_frame, textvariable= e_value, width=12, font=('Arial', 8))
                self.__widgets["matrix coords"][i][j] = e_value
                e.grid(row=i, column=j)
                e.insert(tk.END, "")
        # Create canvas window to hold the table_frame.      
        canvas.create_window((0,0), window=table_frame, anchor=tk.NW)        
        table_frame.update_idletasks()  # Needed to make bbox info available.        
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.        

        # Define the scrollable region as entire canvas with only the desired        
        # number of rows and columns displayed.        
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        rows_displayed = 8 if self.__n >= 8 else self.__n

        dw = int((w/self.__n) * rows_displayed)
        dh = int((h/self.__n) * self.__n)     
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        
