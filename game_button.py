from tkinter import Label
import game_reboot
import minesweeper_graphic_resources as ms_gr


class Game_Button(Label):
    
    def __init__(self, master, **kw):
        Label.__init__(self,master=master, **kw)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.motion)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.default_image = self["image"]

    def on_click(self, event):
        self.motion(event)
        return "break"

    def motion(self, event):
        if self == event.widget.winfo_containing(event.x_root, event.y_root):
            self.config(image= ms_gr.GUI.game_button[4])            
        else:
            self.config(image= ms_gr.GUI.game_button[0])    
        return "break"        

    def on_release(self, event):
        if self == event.widget.winfo_containing(event.x_root, event.y_root):
            self.config(image= self.default_image)    
            game_reboot.restart_game(self)
            game_reboot.restart_current_size(self)
            return "break"
    
    def change_image(self, index):
        self.config(image= ms_gr.GUI.game_button[index])  

