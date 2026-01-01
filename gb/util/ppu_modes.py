from enum import Enum

class PPU_MODES(Enum):
    """
    contains the various modes of the PPU and their cycle counts.
    see: https://gbdev.io/pandocs/Rendering.html
    """
    # Mode 0
    H_BLANK = 204

    # Mode 1
    # Each scanline takes 456 cycles
    # V Blank lasts for 10 scanlines (144 to 153)
    V_BLANK = 4560

    # Mode 2
    OAM_SCAN = 80

    # Mode 3
    VRAM_READ = 172

def example_usage():
    # Usage example
    ppu_mode = PPU_MODES.H_BLANK
    print(f"Current PPU Mode: {ppu_mode.name}")
    if ppu_mode == PPU_MODES.H_BLANK:
        print("The PPU is currently in H-Blank mode.")