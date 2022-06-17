import cell
import widget_navigation as wdgt_nav
import minesweeper_gui as ms_gui

def restart_game(widget):
    cell.Cell.restart()   
    mine_counter = wdgt_nav.get_mine_counter(widget)
    mine_counter.update_mine_counter()
    timer = wdgt_nav.get_timer(widget)
    timer.restart()

def restart_current_size(widget):
    game_frame = wdgt_nav.get_game_frame(widget)
    bot_frame = game_frame.master
    game_frame.destroy()
    ms_gui.new_game(bot_frame)