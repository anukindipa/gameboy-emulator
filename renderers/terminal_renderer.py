import curses
import numpy as np

class TerminalRenderer():
    def __init__(self):
        # TODO: initialize curses and set up the terminal for rendering
        self.framebuffer = np.zeros((144, 160), dtype=np.uint8)  # 144 rows x 160 cols
        
        # self.stdscr = curses.initscr()
        # self.stdscr.nodelay(True)  # non-blocking input

    def render_scanline(self, ppu):
        # TODO: implement
        print(f"Rendering scanline: {ppu.ly}")
        
    def get_input(self):
        # input_char =  self.stdscr.getch()
        # return chr(input_char) if input_char != -1 else None
        return