import sys
import time

def test_one():
    # sys.stdout.write("Hello\n")
    # sys.stdout.flush()

    # clear screen
    print("\x1b[2J")

    for i in range(10):
        print(f"\x1b[H Line {i+1}")
        time.sleep(0.5)
        print("\x1b[2J")

    done_str = """\n-------------------\n \n DONE!     \n \n-------------------\n"""

    print("\x1b[H",done_str)

# Braille dot mapping for a 2x4 block:
# (x,y) in block -> bit
# left column:  (0,0)=dot1, (0,1)=dot2, (0,2)=dot3, (0,3)=dot7
# right column: (1,0)=dot4, (1,1)=dot5, (1,2)=dot6, (1,3)=dot8
_BRAILLE_BITS = {
    (0, 0): 0x01,  # dot 1
    (0, 1): 0x02,  # dot 2
    (0, 2): 0x04,  # dot 3
    (0, 3): 0x40,  # dot 7
    (1, 0): 0x08,  # dot 4
    (1, 1): 0x10,  # dot 5
    (1, 2): 0x20,  # dot 6
    (1, 3): 0x80,  # dot 8
}

def render_braille(frame_144x160, threshold=2):
    """
    frame_144x160: 144 rows x 160 cols, values 0..3 (GB shades) OR 0..255 grayscale.
    threshold: pixels >= threshold are treated as "on" (darker).
    Returns a string with ANSI cursor-home to overwrite the terminal.
    """
    h, w = 144, 160
    out_lines = []
    # Pack 2x4 pixels into one braille char -> 80x36
    for y in range(0, h, 4):
        line_chars = []
        for x in range(0, w, 2):
            bits = 0
            for dy in range(4):
                for dx in range(2):
                    py = y + dy
                    px = x + dx
                    v = frame_144x160[py][px]
                    # If grayscale 0..255, you can threshold around ~128:
                    on = (v >= threshold)  # for GB shades 0..3
                    if on:
                        bits |= _BRAILLE_BITS[(dx, dy)]
            line_chars.append(chr(0x2800 + bits))
        out_lines.append("".join(line_chars))
    # Move cursor to top-left and draw
    return "\x1b[H" + "\n".join(out_lines)

def main_loop(get_frame_fn, fps=60):
    # Clear screen, hide cursor
    sys.stdout.write("\x1b[2J\x1b[H\x1b[?25l")
    sys.stdout.flush()
    dt = 1.0 / fps
    try:
        while True:
            frame = get_frame_fn()  # should return 144x160
            sys.stdout.write(render_braille(frame, threshold=2))
            sys.stdout.flush()
            time.sleep(dt)
    finally:
        # Show cursor again
        sys.stdout.write("\x1b[?25h")
        sys.stdout.flush()

# Example dummy source (replace with your PPU framebuffer)
def dummy_frame():
    # Simple moving gradient demo without numpy
    t = time.time()
    frame = [[0]*160 for _ in range(144)]
    for y in range(144):
        for x in range(160):
            v = (x + int(t*30)) % 4
            frame[y][x] = v
    return frame

if __name__ == "__main__":
    main_loop(dummy_frame)
