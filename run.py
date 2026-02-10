from gb.mbc.mbc0 import MBC0
from gb.mbc.mbc1 import MBC1
from gb.mmu import MMU
from gb.cpu.cpu import CPU
from gb.ppu import PPU
from gb.inputs import InputHandler
# from renderers.terminal_renderer import TerminalRenderer
# from renderers.pygame_renderer import PygameRenderer
# from renderers.vram_pygame_renderer import VramPygameRenderer
from renderers.sdl_renderer import SDLRenderer

def run():
    # Initialize components

    # Tetris
    # Using MBC0 for no bank switching
    # No ROM loaded for this example
    mbc = MBC0("./roms/tetris.gb")

    # Test ROMs
    # mbc = MBC0("./tests/cpu_test_roms/cpu_instrs.gb")
    # mbc = MBC0("./tests/cpu_test_roms/individual/06-ld r,r.gb")

    mmu = MMU(mbc=mbc)

    # renderer = TerminalRenderer()
    # renderer = PygameRenderer(scale=3)
    renderer = SDLRenderer(scale=3)
    # renderer = VramPygameRenderer(scale=3)
    cpu = CPU(mmu=mmu)
    ppu = PPU(mmu=mmu, renderer=renderer)
    input_handler = InputHandler(cpu)

    # Main emulation loop (simplified)
    while True:
        # Execute one CPU instruction
        cycles = cpu.step()
        cpu.mmu.timer.step(cycles)  # Update timers with the number of cycles taken by CPU

        # Step PPU with the number of cycles taken by CPU
        ppu.step(cycles)


        # Read and handle input
        input_handler.handle_input(renderer.get_input())

if __name__ == "__main__":
    run()
