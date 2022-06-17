import tkinter as tk
import settings
import minesweeper_graphic_resources as ms_gr
import mouse_interface as m_i
from game_button import Game_Button
from minesweeper_counter import Mine_Counter, Time_Counter
import cell


def create_top_half(parent_frame):
    WIDTH = settings.WIDTH()
    
    top_frame = tk.Frame(
        parent_frame,
        width= WIDTH,
        height=52  
    )
    top_frame.place(x=0, y=0)

    nw_label = tk.Label(
        top_frame,
        image= ms_gr.GUI.top_frame_template[0], 
        borderwidth = 0, 
        highlightthickness=0,
    )
    nw_label.place(x=0, y=0)

    ne_label = tk.Label(
        top_frame,
        image= ms_gr.GUI.top_frame_template[1], 
        borderwidth = 0, 
        highlightthickness=0,
    )
    ne_label.place(x= WIDTH - 58, y=0)

    center_label = tk.Label(
        top_frame,
        image= ms_gr.GUI.top_frame_template[2], 
        borderwidth = 0, 
        highlightthickness=0,
    )
    center_label.place(x= WIDTH*0.5 - 16, y=0)

    create_top_widgets(top_frame)

    COLUMNS = settings.COLUMNS()
    if COLUMNS > 8:
        center_left =tk.Frame(
        top_frame,
        width= (WIDTH - 148)*0.5,
        height= 52 
        )
        center_left.place(x=58, y=0)

        center_right =tk.Frame(
        top_frame,
        width= (WIDTH - 148)*0.5,
        height= 52 
        )
        center_right.place(x= 90 + (WIDTH - 148)*0.5, y=0)
        if COLUMNS % 2 == 1: 
            l_half_cell = tk.Label(
                center_left,
                image= ms_gr.GUI.top_frame_template[4], 
                borderwidth = 0, 
                highlightthickness=0,
                )            
            l_half_cell.pack(side="left")

            r_half_cell = tk.Label(
                center_right,
                image= ms_gr.GUI.top_frame_template[4], 
                borderwidth = 0, 
                highlightthickness=0,
                )            
            r_half_cell.pack(side="left")
        ms_gr.GUI.img_repeat(center_left, ms_gr.GUI.top_frame_template[3], "horizontal")
        ms_gr.GUI.img_repeat(center_right, ms_gr.GUI.top_frame_template[3], "horizontal")

def create_top_widgets(parent_frame):
    mine_counter = Mine_Counter(
        parent_frame.winfo_children()[0],
        highlightthickness=0,
        bd= 0
        )
    mine_counter.place(x=16, y=14, height= 23, width= 39)

    time_counter = Time_Counter(
        parent_frame.winfo_children()[1],
        highlightthickness=0,
        bd= 0
        )
    time_counter.place(x=3, y=14, height= 23, width= 39)

    game_button = Game_Button(
        parent_frame.winfo_children()[2],
        image = ms_gr.GUI.game_button[0],
        highlightthickness=0,
        bd= 0
        )
    game_button.place(x=3, y=13)

def create_bottom_half(parent_frame):
    WIDTH = settings.WIDTH()
    HEIGHT = settings.HEIGHT()
    bot_frame = tk.Frame(
        parent_frame,
        width= WIDTH,
        height= HEIGHT - 52  
    )
    bot_frame.place(x= 0, y= 52)

    left_edge = tk.Frame(
        bot_frame,
        width= 10,
        height= HEIGHT - 62  
    )
    left_edge.place(x= 0, y= 0)

    right_edge = tk.Frame(
        bot_frame,
        width= 10,
        height= HEIGHT - 62  
    )
    right_edge.place(x= WIDTH - 10, y= 0 )

    bottom_edge = tk.Frame(
        bot_frame,
        width= WIDTH,
        height= 10 
    )
    bottom_edge.place(x= 0, y= settings.ROWS() * 16)

    cornerless_bottom_edge = tk.Frame(
        bottom_edge,
        width= WIDTH - 20,
        height= 10 
    )
    cornerless_bottom_edge.place(x= 10, y= 0)

    sw_corner = tk.Label(
        bottom_edge,
        image= ms_gr.GUI.bottom[0], 
        borderwidth = 0, 
        highlightthickness=0
    )
    sw_corner.place(x= 0, y= 0)

    se_corner = tk.Label(
        bottom_edge,
        image= ms_gr.GUI.bottom[1], 
        borderwidth = 0, 
        highlightthickness=0
    )
    se_corner.place(x= WIDTH - 10, y= 0)

    ms_gr.GUI.img_repeat(left_edge, ms_gr.GUI.side_border, "vertical")
    ms_gr.GUI.img_repeat(right_edge, ms_gr.GUI.side_border, "vertical")
    ms_gr.GUI.img_repeat(cornerless_bottom_edge, ms_gr.GUI.bottom[2], "horizontal")
    new_game(bot_frame)

    
def new_game(parent_frame):
    game_frame = tk.Frame(
        parent_frame,
        width= settings.WIDTH() - 20,
        height= settings.HEIGHT() - 62  
    )
    game_frame.place(x= 10, y= 0)

    for x in range(settings.COLUMNS()):
        for y in range(settings.ROWS()):
            c = cell.Cell(x,y)
            c.create_btn_object(game_frame)
            c.cell_btn_object.grid(
                column= x,
                row= y
            )

    game_frame.bind_all("<B1-Motion>", m_i.tracking)
    game_frame.bind_all("<ButtonPress-1>", m_i.on_lclick)
    game_frame.bind_all("<ButtonPress-3>", m_i.on_rclick)
    game_frame.bind_all("<ButtonRelease-1>", m_i.release)
    game_frame.bind_all("<ButtonRelease-3>", m_i.release)

def initialize_game(parent_frame):
    board = tk.Frame(
        parent_frame,
        width= settings.WIDTH(),
        height= settings.HEIGHT()  
    )
    board.place(x=0, y=0)
    create_top_half(board)
    create_bottom_half(board)
