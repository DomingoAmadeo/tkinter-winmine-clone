import tkinter as tk
import settings
import game_reboot
import minesweeper_gui as ms_gui
import widget_navigation as wdgt_nav

def new_difficulty(difficulty, master_window):
    if difficulty != settings.DIFFUCULTY() or difficulty == 4:
        settings.get_difficulty(difficulty)
        game_reboot.restart_game(master_window)
        master_window.winfo_children()[1].destroy()
        master_window.geometry(f"{str(settings.WIDTH())}x{str(settings.HEIGHT())}")
        ms_gui.initialize_game(master_window)
    else:
        game_btn = wdgt_nav.get_game_button_from_None()
        game_btn.change_image(0)
        game_reboot.restart_game(master_window)
        game_reboot.restart_current_size(master_window)

def show_records(parent):
    parent_x, parent_y = parent.winfo_x(), parent.winfo_y()
    records_window = tk.Toplevel(parent)
    records_window.geometry(f"255x153+{parent_x + 4}+{parent_y + 96}")
    records_window.title("Fastest Mine Sweepers")
    records_window.resizable(False, False)    
    records_window.bind("<ButtonPress-1>", return_break)
    records_window.bind("<ButtonPress-3>", return_break)

    grid_frame = tk.Frame(records_window, width=249)
    grid_frame.pack(side="top", padx=(6,0), pady=(20,0), fill='x')

    records_matrix = []

    for key, value in settings.RECORDS().items():
        difficulty = [key.capitalize()+":"]
        time, name = value.split(",")
        row = [difficulty, time + " seconds", name]
        records_matrix.append(row)

    for row in records_matrix:
        for column in row:
            tk.Label(grid_frame, text=column[:12]).grid(sticky="w", column= row.index(column), row= records_matrix.index(row), padx=3)

    button_frame = tk.Frame(records_window)
    button_frame.pack(side="top")
    reset_button =  tk.Button(button_frame, text="Reset Scores", bd= 1, command=lambda: reset_records(grid_frame))
    reset_button.pack(side="left", padx= (0,31), pady= 14)
    ok_button =  tk.Button(button_frame, text="OK", width= 5, bd= 1, command=lambda: destroy_window(records_window, parent))
    ok_button.pack(side="left", padx= (31,0), pady= 14)
            
            
    records_window.wait_visibility()
    records_window.grab_set()
    records_window.protocol("WM_DELETE_WINDOW", lambda: destroy_window(records_window, parent))
    records_window.transient(parent)
    parent.attributes("-disabled", 1)
    parent.wait_window(records_window)

def reset_records(parent_frame):
    time = "999"
    name = "Anonymus"
    for old_time, old_name in zip(parent_frame.grid_slaves(column= 1), parent_frame.grid_slaves(column= 2)):
        old_time["text"] = time + " seconds"
        old_name["text"] = name
    settings.update("records", "beginner", f"{time},{name}")
    settings.update("records", "intermediate", f"{time},{name}")
    settings.update("records", "expert", f"{time},{name}")
    settings.update("records", "nightmare", f"{time},{name}")

def custom_difficulty(parent):
    parent_x, parent_y = parent.winfo_x(), parent.winfo_y()
    custom_window = tk.Toplevel(parent)
    custom_window.geometry(f"195x138+{parent_x + 4}+{parent_y + 54}")
    custom_window.title("Custom field")
    custom_window.resizable(False, False)    
    custom_window.bind("<ButtonPress-1>", lambda event: focus_color_manager(entries))
    custom_window.bind("<ButtonPress-3>", lambda event: focus_color_manager(entries))

    frame = tk.Frame(custom_window, width=167, height=70)
    frame.pack(padx=(12, 16), pady=(31, 37))
    left_frame = tk.Frame(frame, width=93, height=70)
    left_frame.pack(side="left")
    right_frame = tk.Frame(frame, width=74, height=70)
    right_frame.pack(side="left")   

    labels = [None, None, None]
    label_text = ["Height: ", "Width: ", "Mines: "]

    entries = [None, None, None]
    entry_placeholder = [settings.ROWS(), settings.COLUMNS(), settings.MINES()]

    for i in range (3):
        labels[i] = tk.Label(left_frame, text= label_text[i])
        labels[i].grid(column= 0, row= i)    
        grid_frame = tk.Frame(left_frame, bg= "#7a7a7a") 
        grid_frame.grid(column= 1, row= i, pady= 2, padx=(5, 0))    
        entries[i] = tk.Entry(grid_frame, width=6, relief="flat", bd=0)
        entries[i].insert(0, entry_placeholder[i])
        entries[i].pack(pady= 1, padx=1)
    
    ok_button =  tk.Button(right_frame, text="OK", width= 52, command=lambda: accept(entries, custom_window, parent))
    ok_button.pack(side="top", padx= (23, 0), pady= 0)
    cancel_button =  tk.Button(right_frame, text="Cancel", width= 52, command=lambda: dismiss(custom_window, parent))
    cancel_button.pack(side="top", padx= (23, 0), pady=(18,1))
    
    custom_window.wait_visibility()
    custom_window.grab_set()
    custom_window.protocol("WM_DELETE_WINDOW", lambda: dismiss(custom_window, parent))
    custom_window.transient(parent)
    parent.attributes("-disabled", 1)
    parent.wait_window(custom_window)
   
def focus_color_manager(widget_list):
    for widget in widget_list:
        if widget == widget.focus_get():
            widget.master.configure(bg="#0076d7")
        else:
            widget.master.configure(bg="#7a7a7a")
    return "break"

def validate(new_settings):
    min_values = [1, 8, 1]
    max_values = [35, 80, 2380]
    
    for i in range(3):
        if new_settings[i].isdecimal():
            new_settings[i] = int(new_settings[i])
            if new_settings[i] < min_values[i]:
                new_settings[i] = min_values[i]
            elif new_settings[i] > max_values[i]:
                new_settings[i] = max_values[i]
        else:
            new_settings[i] = min_values[i]

    max_mines = new_settings[0]*new_settings[1]*85//100
    if new_settings[2] > max_mines and max_mines > 0:
        new_settings[2] = max_mines
    return new_settings

def check_records(widget):
    diff = settings.DIFFUCULTY()
    if diff < 4:
        difficulty = ["beginner", "intermediate", "expert", "nightmare"][diff]
        previous_time, name = settings.RECORDS()[difficulty].split(",")
        previous_time = int(previous_time)
        timer = wdgt_nav.get_timer(widget)
        new_time =  timer.seconds_passed
        if new_time < previous_time:
            new_time = str(new_time)
            new_best_time(widget, difficulty, new_time, name)
    
def new_best_time(parent, difficulty, new_time, name):
    parent_x, parent_y = parent.winfo_x(), parent.winfo_y()
    record_dialog = tk.Toplevel(parent, relief="raised", bd= 2)
    record_dialog.geometry(f"156x169+{parent_x + 90}+{parent_y + 96}")
    record_dialog.wm_overrideredirect(True)
    record_dialog.resizable(False, False)    
    record_dialog.bind("<ButtonPress-1>", return_break)
    record_dialog.bind("<ButtonPress-3>", return_break)
    record_dialog.bind('<Escape>', lambda event: dismiss_record_dialog(record_dialog, parent, difficulty, new_time, input_widget.get()))
    record_dialog.bind("<Return>", lambda event: dismiss_record_dialog(record_dialog, parent, difficulty, new_time, input_widget.get()))

    text_label = tk.Label(record_dialog, text=f"You have the fastest time\nfor {difficulty} level.\nPlease enter your name.")
    text_label.pack(side="top")

    ok_button = tk.Button(record_dialog, text="OK", command=lambda: dismiss_record_dialog(record_dialog, parent, difficulty, new_time, input_widget.get()))
    ok_button.pack(side="bottom",fill="x", padx= 50, pady=(0,24))

    input_widget = tk.Entry(record_dialog)
    input_widget.insert(0, name)
    input_widget.selection_range(0,"end")
    input_widget.focus()
    input_widget.pack(side="bottom", pady=(0,13))

    record_dialog.wait_visibility()
    record_dialog.grab_set()
    record_dialog.transient(parent)
    record_dialog.attributes("-topmost", True)
    parent.attributes("-disabled", 1)
    parent.wait_window(record_dialog)

def accept(entry_list, widget, parent):
    input = [widget.get() for widget in entry_list]
    values = validate(input)
    settings.update("current","rows",str(values[0]))
    settings.update("current","columns",str(values[1]))
    settings.update("current","mines",str(values[2]))
    dismiss(widget, parent)

def dismiss (widget, parent):
    settings.update("settings", "difficulty", "4")
    new_difficulty(4, parent)
    destroy_window(widget, parent)

def dismiss_record_dialog(toplevel, parent, key, new_time, name):
    value = new_time + "," + name
    settings.update("records", key, value)
    destroy_window(toplevel, parent)
    show_records(parent)

def destroy_window(widget, parent):
    parent.attributes("-disabled", 0)
    widget.grab_release()
    widget.destroy()

def return_break(event = 0):
    return "break"
