import cell
import widget_navigation as wdgt_nav


focused_widgets = [None]
is_b1_pressed = False
is_b3_pressed = False
is_smiley_pressed = False

def surrounding_widgets(widget):
    if check_for_error(widget):
        return [None]
    widget_list = []
    w_cell = wdgt_nav.cellify(widget)
    cells = w_cell.surrounding_cells
    cells.append(w_cell)
    for cell in cells:
        widget_list.append(wdgt_nav.widget_from_cell(cell))   
    return widget_list

def enter_widgets(widget_list):
    for widget in widget_list:                                  
                widget.event_generate("<<B1-Enter>>")  

def leave_widgets(previously_focused, newly_focused):
    for old in previously_focused:
        if old not in newly_focused:
            old.event_generate("<<B1-Leave>>")

def on_rclick(event):
    global is_b3_pressed
    is_b3_pressed = True
    widget = wdgt_nav.widget_from_mouse_position(event)
    if is_b1_pressed:
        tracking(event)                           
    else:        
        mine_counter = wdgt_nav.get_mine_counter(widget)
        widget.event_generate("<<B3-Press>>")
        mine_counter.event_generate("<<Update-Counter>>")

def on_lclick(event):
    global is_b1_pressed
    is_b1_pressed = True
    if cell.Cell.game_state < 1:
        game_btn = wdgt_nav.get_game_button_from_None()
        game_btn.change_image(1)
    tracking(event)

def tracking(event):
    global focused_widgets

    if is_b1_pressed:    
        widget = wdgt_nav.widget_from_mouse_position(event)  
        if not is_b3_pressed:
            candidates = [widget]       
        else:
            candidates = surrounding_widgets(widget)

        if focused_widgets != candidates:                                        
            if focused_widgets[0]:
                leave_widgets(focused_widgets, candidates)
            focused_widgets = candidates
            if focused_widgets[0]:              
                enter_widgets(focused_widgets)

def release(event):
    global focused_widgets
    if is_b1_pressed:
        widget_released = wdgt_nav.widget_from_mouse_position(event)
        if wdgt_nav.is_widget_in_game_frame(widget_released) and cell.Cell.game_state == -1:            
            cell.Cell.game_state = 0
            wdgt_nav.get_timer(widget_released).event_generate("<<Start-Timer>>")
        if is_b3_pressed:
            widget_released.event_generate("<<B1-Chord>>")   
        else:
            for widget in focused_widgets:
                if not check_for_error(widget):
                    widget.event_generate("<<B1-Release>>")
        focused_widgets = [None]
        game_btn = wdgt_nav.get_game_button_from_None()
        if cell.Cell.game_state < 1:
            game_btn.change_image(0)
            return release_buttons()
        elif cell.Cell.game_state == 2:
            game_btn.change_image(3)
            return release_buttons()
        elif cell.Cell.game_state == 1:
            game_btn.change_image(2)
            mine_counter = wdgt_nav.get_mine_counter(widget_released)
            mine_counter.event_generate("<<Update-Counter>>")
            release_buttons()
            game_btn.winfo_toplevel().event_generate("<<Check-Records>>")
    release_buttons()

def release_buttons():
    global is_b1_pressed
    global is_b3_pressed
    is_b3_pressed = False  
    is_b1_pressed = False



def check_for_error(widget):
    if widget == None or not hasattr(widget,'grid_info') or 'in' not in widget.grid_info():
        return True