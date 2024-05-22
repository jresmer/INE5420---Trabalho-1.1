# import tkinter as tk


# def draw(coordinates: tuple) -> tuple:
        
#         window_xmin, window_ymin, window_xmax, window_ymax = [0, 0, 1280, 900]
#         vp_xmin, vp_ymin, vp_xmax, vp_ymax = [0, 0, 1280, 900]
#         # calculating points between p1 and p4
#         for i in range((len(coordinates))):
#              x, y = coordinates[i]
#              x = (x - window_xmin) * (vp_xmax - vp_xmin) / (window_xmax - window_xmin)
#              y = (1 - (y - window_ymin)/(window_ymax - window_ymin)) * (vp_ymax - vp_ymin)
#              coordinates[i] = (x, y)

#         p1, p2, p3, p4 = coordinates
#         coords = []
#         t_to_be_calculated = list(range(0,1001))
#         for i in range(len(t_to_be_calculated)):
#             t_to_be_calculated[i] *= (1/1000)
#         for t in t_to_be_calculated:
#             p = [0, 0]
#             for i in range(len(p)):

#                 p[i] = p1[i] * (-1*t**3 + 3*t**2 - 3*t + 1) + p2[i] * (3*t**3 - 6*t**2 + 3*t) \
#                     + p3[i] * (-3*t**3 + 3*t**2) + p4[i] * (t**3)
                
#             coords.append(p)
#         return coords
    
# curved_line = draw([(170,180),(200,120),(375,120), (380,240)])
                                  
# root = tk.Tk()
# root.geometry("1280x900")
# canvas = tk.Canvas(master=root, height=900, width=1280, bg="white",relief="ridge")
# canvas.place(x=0,y=0)

# for i in range(0, len(curved_line) - 1):
#     x0, y0 = curved_line[i]
#     x1, y1 = curved_line[i+1]
    
#     canvas.create_line(x0, y0, x1, y1, fill="green")
    
# root.mainloop()

# Function to return x-value of point of intersection of two lines
def x_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)
    den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return num/den

# Function to return y-value of point of intersection of two lines
def y_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)
    den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return num/den

# Function to clip all the edges w.r.t one clip edge of clipping area
def clip(poly_points, poly_size, x1, y1, x2, y2):
    new_coords = []

    # (ix,iy),(kx,ky) are the co-ordinate values of the points
    for i in range(poly_size):
        # i and k form a line in polygon
        k = (i+1) % poly_size
        ix, iy = poly_points[i]
        kx, ky = poly_points[k]

        # Calculating position of first point w.r.t. clipper line
        i_pos = (x2-x1) * (iy-y1) - (y2-y1) * (ix-x1)

        # Calculating position of second point w.r.t. clipper line
        k_pos = (x2-x1) * (ky-y1) - (y2-y1) * (kx-x1)

        # Case 1 : When both points are inside
        if i_pos < 0 and k_pos < 0:
            # Only second point is added
            new_coords.append((kx, ky))

        # Case 2: When only first point is outside
        elif i_pos >= 0 and k_pos < 0:
            # Point of intersection with edge and the second point is added
            coord = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                     y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_coords.append(coord)
            new_coords.append((kx, ky))

        # Case 3: When only second point is outside
        elif i_pos < 0 and k_pos >= 0:
            # Only point of intersection with edge is added
            coord = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                     y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_coords.append(coord)

    return new_coords

# Function to implement Sutherland–Hodgman algorithm
def suthHodgClip(clipped_polygon, clipper_polygon):
    clipper_size = len(clipper_polygon)
    # i and k are two consecutive indexes
    for i in range(clipper_size):
        k = (i+1) % clipper_size

        # We pass the current array of vertices, it's size and the end points of the selected clipper line
        clipped_polygon = clip(clipped_polygon, len(clipped_polygon), clipper_polygon[i][0],
                               clipper_polygon[i][1], clipper_polygon[k][0],
                               clipper_polygon[k][1])

    # Printing vertices of clipped polygon
    # for i in range(len(clipped_polygon)):
    #     print('(', (clipped_polygon[i][0]), ', ', clipped_polygon[i][1], ')')
    return clipped_polygon


# poly_points = [(10,20),
#                (32,70),
#                (58, 40),
#                (60,80),
#                (90,80),
#                (110,200),
#                (98, 10),
#                (21, 10),
#                (10,20)]
# clipper_points = [(40,8), (40,70), (90,70), (90,8)]
# suthHodgClip(poly_points, clipper_points)
