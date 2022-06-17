import cell

def widget_from_mouse_position(event):
    return event.widget.winfo_containing(event.x_root, event.y_root)

def cellify(widget):
    return cell.Cell.get_cell_by_axis(widget.grid_info()['column'], widget.grid_info()['row'])

def widget_from_cell(cell):
    return cell.cell_btn_object

def get_mine_counter(widget):
    top_frame = get_top_frame(widget)
    return top_frame.winfo_children()[0].winfo_children()[0]

def get_timer(widget):
    top_frame = get_top_frame(widget)
    return top_frame.winfo_children()[1].winfo_children()[0]

def get_game_button_from_None():
    widget = widget_from_cell(cell.Cell.all[0])
    top_frame = get_top_frame(widget)
    return top_frame.winfo_children()[2].winfo_children()[0]

def get_top_frame(widget):
    first_frame = get_first_frame(widget)
    return first_frame.winfo_children()[0]    

def get_game_frame(widget):
    first_frame = get_first_frame(widget)
    game_frame = first_frame.winfo_children()[1].winfo_children()[3]  #.!frame.!frame2.!frame4
    return game_frame 

def is_widget_in_game_frame(widget):
    try:
        return widget.master == get_game_frame(widget)
    except:
        return False

def get_first_frame(widget):
    return widget.winfo_toplevel().winfo_children()[1]