import tkinter as tk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class GUI():
    counter_numbers = None
    cell_images = None
    bottom = None
    game_button = None
    side_border = None
    top_frame_template = None

    def __init__(self):
        super().__init__()   
        self.numbers = tk.PhotoImage(file=resource_path("imgs\\numbers.png"))
        self.cell_graphic = tk.PhotoImage(file=resource_path("imgs\\cells.png"))
        self.bottom_graphic = tk.PhotoImage(file=resource_path("imgs\\bottom-graphics.png"))
        self.top_frame_graphic = tk.PhotoImage(file=resource_path("imgs\\top-frame-template.png"))
        self.top_center_graphic = tk.PhotoImage(file=resource_path("imgs\\top-center-template.png"))
        self.smiley_button = tk.PhotoImage(file=resource_path("imgs\\button-face.png"))
        self.top_center_filler = self.subimage(116, 0, 132, 52, self.top_frame_graphic)
        self.top_center_filler_small = self.subimage(124, 0, 132, 52, self.top_frame_graphic)
        self.bottom_border = self.subimage(20, 0, 36, 10, self.bottom_graphic)
        GUI.counter_numbers = [self.subimage(13*i,0,(13*(i+1)),23, self.numbers) for i in range(12)]
        GUI.cell_images = [self.subimage(0,16*i,16,(16*(i+1)), self.cell_graphic) for i in range(16)]
        GUI.bottom = [self.subimage(10*i,0,(10*(i+1)),10, self.bottom_graphic) for i in range(2)]
        GUI.game_button = [self.subimage(26*i,0,(26*(i+1)),26, self.smiley_button) for i in range(5)]
        GUI.top_frame_template = [self.subimage(58*i,0,(58*(i+1)),52, self.top_frame_graphic) for i in range(2)]
        GUI.top_frame_template.append(self.top_center_graphic)
        GUI.top_frame_template.append(self.top_center_filler)
        GUI.top_frame_template.append(self.top_center_filler_small)
        GUI.bottom.append(self.bottom_border)
        GUI.side_border = tk.PhotoImage(file=resource_path("imgs\\side-border.png"))

    def subimage(self, l, t, r, b, spritesheet):
            #print(l,t,r,b)
            new_img = tk.PhotoImage()
            new_img.tk.call(new_img, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
            return new_img

    def img_repeat(frame, img, direction):
        if direction == "vertical":
            n = int(frame.winfo_reqheight()/ img.height())
            for _ in range (n):
                label = tk.Label(frame, image=img, borderwidth = 0, highlightthickness=0)
                label.pack(side="top")
        else:
            n = int(frame.winfo_reqwidth()/ img.width())
            for _ in range (n):
                label = tk.Label(frame, image=img, borderwidth = 0, highlightthickness=0)
                label.pack(side="left")
                
                
                