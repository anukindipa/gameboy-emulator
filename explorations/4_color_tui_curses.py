'''
ANSI escape code version - NOT Compatible with curses

# set foreground color: \033[38;5;<n>m
# set background color: \033[48;5;<n>m
# set foreground and background color: \033[38;5;<fg>;48;5;<bg>m
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

# print("\033[31;44m▀▄▀▀▀▀▄▄▄▀▀▄▄▄▀▀▄\033[0m")  # red on blue
# print("\033[0;44m▀▄▀▀▀▀▄▄▄▀▀▄▄▄▀▀▄\033[0m")  # red on blue

Ansi escape codes for 4-shade grayscale
up_0 = "38;2;0;0;0"
up_1 = "38;2;63;63;63"
up_2 = "38;2;170;170;170"
up_3 = "38;2;255;255;255"

down_0 = "48;2;0;0;0"
down_1 = "48;2;63;63;63"
down_2 = "48;2;170;170;170"
down_3 = "48;2;255;255;255"

shades = [ 
   [f"\033[{up_0};{down_0}m▀\033[0m", f"\033[{up_0};{down_1}m▀\033[0m", f"\033[{up_0};{down_2}m▀\033[0m", f"\033[{up_0};{down_3}m▀\033[0m",],
   [f"\033[{up_1};{down_0}m▀\033[0m", f"\033[{up_1};{down_1}m▀\033[0m", f"\033[{up_1};{down_2}m▀\033[0m", f"\033[{up_1};{down_3}m▀\033[0m",],
   [f"\033[{up_2};{down_0}m▀\033[0m", f"\033[{up_2};{down_1}m▀\033[0m", f"\033[{up_2};{down_2}m▀\033[0m", f"\033[{up_2};{down_3}m▀\033[0m",],
   [f"\033[{up_3};{down_0}m▀\033[0m", f"\033[{up_3};{down_1}m▀\033[0m", f"\033[{up_3};{down_2}m▀\033[0m", f"\033[{up_3};{down_3}m▀\033[0m",],
]
def print_shades():
    for row in shades:
        print("".join(row))

def print_square():
    import random
    for i in range(20):
        for j in range(40):
            shade = random.randint(0,15)
            print(shades[shade//4][shade%4], end="")
        print()
'''

# Curses version

import curses
import random


screen_buffer = [[(((i+j)*4))%16 for i in range(160)] for j in range(72)]

def print_shades_curses(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.idcok(False)
    stdscr.idlok(False)
    stdscr.erase()
    curses.start_color()

    curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_color(curses.COLOR_RED, 333, 333, 333)
    curses.init_color(curses.COLOR_MAGENTA, 667, 667, 667)
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)

    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_MAGENTA)
    curses.init_pair(11, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(14, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(16, curses.COLOR_WHITE, curses.COLOR_WHITE)
            
    for i in range(72):
        for j in range(160):
            stdscr.addstr(i, j, "▀", curses.color_pair(screen_buffer[i][j]+1))
            tmp = screen_buffer[-1]
            screen_buffer[1:] = screen_buffer[:-1]
            screen_buffer[0] = tmp
    
    
    stdscr.refresh()
    time.sleep(1/3)



import time
if __name__ == "__main__":
    for i in range(60):
        curses.wrapper(print_shades_curses)