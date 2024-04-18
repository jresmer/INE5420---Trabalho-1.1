import tkinter as tk


def draw(coordinates: tuple) -> tuple:
        
        window_xmin, window_ymin, window_xmax, window_ymax = [0, 0, 1280, 900]
        vp_xmin, vp_ymin, vp_xmax, vp_ymax = [0, 0, 1280, 900]
        # calculating points between p1 and p4
        for i in range((len(coordinates))):
             x, y = coordinates[i]
             x = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
             y = (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
             coordinates[i] = (x, y)

        p1, p2, p3, p4 = coordinates
        coords = []
        t_to_be_calculated = list(range(0,1001))
        for i in range(len(t_to_be_calculated)):
            t_to_be_calculated[i] *= (1/1000)
        for t in t_to_be_calculated:
            p = [0, 0]
            for i in range(len(p)):

                p[i] = p1[i] * (-1*t**3 + 3*t**2 - 3*t + 1) + p2[i] * (3*t**3 - 6*t**2 + 3*t) \
                    + p3[i] * (-3*t**3 + 3*t**2) + p4[i] * (t**3)
                
            coords.append(p)
        return coords
    
curved_line = draw([(170,180),(200,120),(375,120), (380,240)])
                                  
root = tk.Tk()
root.geometry("1280x900")
canvas = tk.Canvas(master=root, height=900, width=1280, bg="white",relief="ridge")
canvas.place(x=0,y=0)

for i in range(0, len(curved_line) - 1):
    x0, y0 = curved_line[i]
    x1, y1 = curved_line[i+1]
    
    canvas.create_line(x0, y0, x1, y1, fill="green")
    
root.mainloop()
