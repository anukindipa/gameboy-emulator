from gb.mbc.mbc0 import MBC0
from gb.mmu import MMU
from gb.cpu.cpu import CPU
from gb.ppu import PPU
from gb.ppu.terminal_renderer import TerminalRenderer
from gb.ppu.pygame_renderer import PygameRenderer

def run():
    # Initialize components

    # Using MBC0 for no bank switching
    # No ROM loaded for this example
    mbc = MBC0("./roms/tetris.gb")
    mmu = MMU(mbc=mbc)

    # renderer = TerminalRenderer()
    renderer = PygameRenderer(scale=3)
    cpu = CPU(mmu=mmu)
    ppu = PPU(mmu=mmu, renderer=renderer)

    # Main emulation loop (simplified)
    while True:
        # Execute one CPU instruction
        cycles = cpu.step()

        # Step PPU with the number of cycles taken by CPU
        ppu.step(cycles)

        # Read and handle input
        input_chr = renderer.get_input()  
        if input_chr:
            print(f"Input received: {input_chr}")

if __name__ == "__main__":
    run()