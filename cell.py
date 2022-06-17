import settings
import minesweeper_graphic_resources as ms_gr
import random
from tkinter import Label



class Cell:
    all = []
    all_mined = []
    all_flagged = []
    all_visible = set()
    mined = False
    game_state = -1
    mines = None
    
    def __init__(self, x, y, is_mine= False):
        super().__init__()
        self.is_mine = is_mine
        self.is_flagged = False
        self.cell_btn_object = None
        self.x = x 
        self.y = y
        self.is_hidden = True
        Cell.all.append(self)                           # Append the object to the Cell.all list                             

    def create_btn_object(self, location):
        btn = Label(
            location,
            image=ms_gr.GUI.cell_images[0],
            highlightthickness=0,
            bd= 0
        )
        self.cell_btn_object = btn
        self.bind_all_except_m3()
        self.cell_btn_object.bind("<<B3-Press>>", self.right_click_actions)     # M3 action
    
    def bind_all_except_m3(self):        
        self.cell_btn_object.bind("<<B1-Release>>", self.left_click_actions)        # M1 action
        self.cell_btn_object.bind("<<B1-Enter>>", self.cell_enter)                  # Motion enter
        self.cell_btn_object.bind("<<B1-Leave>>", self.cell_leave)                  # Motion leave
        self.cell_btn_object.bind("<<B1-Chord>>", self.chord_click)                 # Chord
        
    def unbind_all_except_m3_and_chord(self):
        self.cell_btn_object.unbind("<<B1-Release>>")
        self.cell_btn_object.unbind("<<B1-Enter>>")
        self.cell_btn_object.unbind("<<B1-Leave>>")             

    def clear_btn(self):
        self.cell_btn_object.unbind("<<B3-Press>>")
        self.unbind_all_except_m3_and_chord()
    
    def right_click_actions(self, event):
        if not self.is_flagged:
            self.flag_cell()
        else:
            self.unflag_cell()

    def left_click_actions(self, event):
        if not self.mined:
            self.randomize_mines()
        if self.is_mine:
            self.show_mines()
        elif self.is_hidden:
            self.show_cell()        

    def chord_click(self, event):
        if not self.is_hidden and self.surrounding_mine_count == self.surrounding_flag_count:
            for cell_obj in self.surrounding_hidden:
                if  not cell_obj.is_flagged:
                    if cell_obj.is_mine:
                        cell_obj.show_mines()
                        continue
                    cell_obj.show_cell()
        else:
            if self.is_hidden and not self.is_flagged:
                self.cell_leave(event)
            for cell_obj in self.surrounding_hidden:
                if not cell_obj.is_flagged:
                    cell_obj.cell_leave(event)

    def cell_enter(self, event):
        self.cell_btn_object.configure(image=ms_gr.GUI.cell_images[15])

    def cell_leave(self, event):
        self.cell_btn_object.configure(image=ms_gr.GUI.cell_images[0]) 

    def flag_cell(self):
        self.is_flagged = True
        self.cell_btn_object.configure(image=ms_gr.GUI.cell_images[1])
        Cell.all_flagged.append(self)
        self.unbind_all_except_m3_and_chord()

    def unflag_cell(self):
        self.cell_btn_object.configure(image=ms_gr.GUI.cell_images[0])
        self.is_flagged = False
        Cell.all_flagged.remove(self)
        self.bind_all_except_m3()

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounding_cells(self):
        cells = []
        for x in range (self.x -1, self.x +2):
            for y in range (self.y -1, self.y +2):
                if not (self.x == x and self.y == y):
                    cells.append(self.get_cell_by_axis(x, y))
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounding_mine_count(self):
        counter = 0
        for cell in self.surrounding_cells:
            if cell.is_mine:
                counter += 1
        return counter

    @property
    def surrounding_flag_count(self):
        counter = 0
        for cell in self.surrounding_cells:
            if cell.is_flagged:
                counter += 1
        return counter

    @property
    def surrounding_hidden(self):
        return [cell for cell in self.surrounding_cells if cell.is_hidden]
        

    def show_cell(self):
        self.is_hidden = False
        mine_count = self.surrounding_mine_count
        self.cleared_image(mine_count)
        self.clear_btn()
        Cell.all_visible.add(self)
        if mine_count == 0:
            for cell_obj in self.surrounding_hidden:
                cell_obj.show_cell()
        if self.check_for_win():
            for mine in Cell.all_mined:
                if mine not in Cell.all_flagged:
                    mine.flag_cell()            
            self.game_end(1)

    def cleared_image(self, number):
        self.cell_btn_object.configure( 
            image= list(reversed(ms_gr.GUI.cell_images))[number]
            )    

    def show_mines(self):
        for cell in Cell.all_mined:
            if self == cell:
                self.cell_btn_object.configure( image=ms_gr.GUI.cell_images[3])
            elif not cell.is_flagged:
                cell.cell_btn_object.configure( image=ms_gr.GUI.cell_images[5])
        for cell in Cell.all_flagged:
            if not cell.is_mine and cell.is_flagged:
                cell.cell_btn_object.configure( image=ms_gr.GUI.cell_images[4])
        self.game_end(2)
        

    def randomize_mines(self):
        Cell.mines = settings.MINES()
        Cell.mined = True
        available_cells = [cell for cell in Cell.all if cell != self]
        Cell.all_mined = random.sample(
            available_cells,
            Cell.mines
        )
        for picked_cell in Cell.all_mined:
            picked_cell.is_mine = True
    
    @staticmethod
    def check_for_win():
        n_mines = len(Cell.all_mined)
        n_visible_tiles = len(Cell.all_visible)
        n_cells = len(Cell.all)
        return n_cells - n_mines == n_visible_tiles

    def game_end(self, n):
        Cell.game_state = n
        for cell in Cell.all:
            cell.clear_btn()
            cell.cell_btn_object.unbind("<<B1-Chord>>")
        

    @classmethod
    def restart(cls):
        for cell in cls.all:
            cell.is_mine = False
            cell.is_flagged = False
            cell.cell_btn_object = None
            cell.is_hidden = True
        cls.game_state = -1
        cls.all_visible.clear()
        cls.all_mined.clear()
        cls.all_flagged.clear()
        cls.mined = False
        cls.mines = None
        cls.all.clear()

    def __repr__(self) -> str:
        return f"Cell ({self.x},{self.y})"