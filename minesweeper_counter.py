import minesweeper_graphic_resources as ms_gr
from tkinter import Label
import cell
import settings

class Counter_Label(Label):
    
    def __init__(self, master, **kw):
        Label.__init__(self,master=master, **kw)
        self.numbers = [
            Label(self, image= ms_gr.GUI.counter_numbers[0] , borderwidth = 0, highlightthickness=0),
            Label(self, image= ms_gr.GUI.counter_numbers[0] , borderwidth = 0, highlightthickness=0),
            Label(self, image= ms_gr.GUI.counter_numbers[0] , borderwidth = 0, highlightthickness=0),
        ]
        for i in range(3):                
            self.numbers[i].place( x= i*13, y= 0)
        
    def get_image_by_number(self, number : int):
        negative = False
        if number > 999:
            number = 999
        if number < 0:
            if number < -99:
                number = -99
            negative = True
            number = abs(number)
        n_of_digits = len(str(number))              
        for i in range(3):
            index = i+1
            if i == n_of_digits:
                self.numbers[-index]['image'] = ms_gr.GUI.counter_numbers[0]
                continue                
            digit = number % 10
            self.numbers[-index]['image'] = ms_gr.GUI.counter_numbers[digit]
            number = number // 10
        if negative:
            self.numbers[0]['image'] = ms_gr.GUI.counter_numbers[10]

class Mine_Counter(Counter_Label):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.remaining_mines = settings.MINES()
        self.bind("<<Update-Counter>>", self.update_mine_counter)
        self.update_mine_counter()

    def update_mine_counter(self, event= None):
        self.remaining_mines = settings.MINES() - len(cell.Cell.all_flagged)
        super().get_image_by_number(self.remaining_mines)    
    
class Time_Counter(Counter_Label):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.seconds_passed = 0
        self.bind("<<Start-Timer>>", self.start_timer)
        self.tracking = None

    def start_timer(self, event):
        self.unbind("<<Start-Timer>>")
        self.add_one_second()

    def add_one_second(self):
        if cell.Cell.game_state == 0:
            self.seconds_passed += 1
            super().get_image_by_number(self.seconds_passed)
            self.tracking = self.after(1000, self.add_one_second)
        else :
            self.cancel()
    
    def cancel(self):
        if self.tracking != None:
            self.after_cancel(self.tracking)
            self.tracking = None

    def restart(self):
        self.cancel()
        self.seconds_passed = 0
        super().get_image_by_number(self.seconds_passed)
        self.bind("<<Start-Timer>>", self.start_timer)

    