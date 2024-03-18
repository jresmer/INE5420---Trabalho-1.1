from tkinter import Canvas

#CLASSE CANVAS COM MOVIMENTO
class MoveCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.objects = []
        self.dx = 0
        self.dy = 0

        self.dt = 25
        self.tick()
              
    def add_object(self, obj):
        self.objects.append(obj)
    
    def tick(self):
        for obj in self.objects:
            self.move(obj, self.dx, self.dy)
        self.after(self.dt, self.tick)
        self.dx = 0
        self.dy = 0

    def change_heading(self, dx, dy):
        self.dx = dx
        self.dy = dy
