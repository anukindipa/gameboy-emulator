from enum import Enum

class PPU_MODES(Enum):
    """
    contains the various modes of the PPU.
    see: https://gbdev.io/pandocs/Rendering.html
    """
    # Mode 0: H-Blank
    H_BLANK = 0

    # Mode 1: V-Blank
    V_BLANK = 1

    # Mode 2: OAM Scan
    OAM_SCAN = 2

    # Mode 3: Pixel Transfer
    PIXEL_TRANSFER = 3

def cycles_for_mode(mode):
    """
    Returns the number of cycles for a given PPU mode.
    """
    if mode == PPU_MODES.H_BLANK:
        return 204
    elif mode == PPU_MODES.V_BLANK:
        return 456
    elif mode == PPU_MODES.OAM_SCAN:
        return 80
    elif mode == PPU_MODES.PIXEL_TRANSFER:
        return 172
    else:
        raise ValueError("Invalid PPU mode")

def example_usage():
    # Usage example
    ppu_mode = PPU_MODES.H_BLANK
    print(f"Current PPU Mode: {ppu_mode.name}")
    if ppu_mode == PPU_MODES.H_BLANK:
        print("The PPU is currently in H-Blank mode.")