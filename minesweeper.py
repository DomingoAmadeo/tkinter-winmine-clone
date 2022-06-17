import tkinter as tk
import settings
import menu_toplevel_logic as m_t_logic
import minesweeper_graphic_resources as ms_gr
import minesweeper_gui as ms_gui


root = tk.Tk()

ms_gr.GUI()

root.geometry(f"{str(settings.WIDTH())}x{str(settings.HEIGHT()+20)}")
root.title("Minesweeper")
root.iconbitmap(ms_gr.resource_path("imgs/ms16windowsxp.ico"))
root.resizable(False, False)
root.bind("<<Check-Records>>", lambda event: m_t_logic.check_records(root))


root.option_add('*tearOff', "false")
menu_bar = tk.Menu(root)
root['menu'] = menu_bar
menu_game = tk.Menu(menu_bar)
menu_bar.add_cascade(menu=menu_game, label='Game')

menu_game.add_command(label="New game", underline=0, accelerator="F2", command=lambda: m_t_logic.new_difficulty(5, root))
menu_game.add_separator()
menu_difficulty = tk.Menu(menu_game)
menu_game.add_cascade(menu=menu_difficulty, label='Difficulty', underline=2)
radio = tk.IntVar()
menu_difficulty.add_radiobutton(label='Beginner', variable=radio, value=0, command=lambda: m_t_logic.new_difficulty(radio.get(), root))
menu_difficulty.add_radiobutton(label='Intermediate', variable=radio, value=1, command=lambda: m_t_logic.new_difficulty(radio.get(), root))
menu_difficulty.add_radiobutton(label='Expert', variable=radio, value=2, command=lambda: m_t_logic.new_difficulty(radio.get(), root))
menu_difficulty.add_radiobutton(label='Nightmare', variable=radio, value=3, command=lambda: m_t_logic.new_difficulty(radio.get(), root))
menu_difficulty.add_radiobutton(label='Custom...', variable=radio, value=4, command=lambda: m_t_logic.custom_difficulty(root))
radio.set(settings.DIFFUCULTY())
menu_game.add_separator()
menu_game.add_command(label="Best Times...", command=lambda: m_t_logic.show_records(root))
menu_game.add_separator()
menu_game.add_command(label="Exit", underline=1, accelerator="Alt+F4", command=lambda: root.destroy())

ms_gui.initialize_game(root)

root.bind("<F2>", lambda event: m_t_logic.new_difficulty(radio.get(), root))

#Keep the window from closing 
root.mainloop()