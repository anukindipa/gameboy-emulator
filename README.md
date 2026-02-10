# gameboy-emulator

An instruction-accurate Game Boy emulator implemented in Python, with performance optimisations and ongoing C++ integration via **pybind11**.  

This project models key hardware components of the original Nintendo Game Boy, including the CPU, memory bus, timers, interrupts, and a scanline-based graphics pipeline.

---

## Demo 

Tetris at 4x speed:

![Tetris Demo](./Assets/Tetris%20Demo.gif)

## Architecture Overview

![Architecture Overview](./Assets/Architecture%20Overview.png)


### How It Works

The emulator synchronizes **CPU execution** with **PPU rendering** each cycle:
- **CPU** executes LR35902 instructions and returns cycle count
- **PPU** advances the scanline-based graphics pipeline by those cycles
- **Input** is processed each frame

**Memory** is managed via a unified MMU supporting ROM/RAM/VRAM/OAM and MBC banking (MBC0, MBC1).

**PPU** renders using 4 scanline modes (OAM Scan → Pixel Transfer → H-Blank → V-Blank), generating output scanline-by-scanline to an SDL2 renderer.

**Interrupts** (V-Blank, LCD STAT, Timer, Joypad) trigger CPU pause/resumption for accurate hardware behavior.

#### Simplified Main Loop (run.py)
```python
while True:
    # Execute one CPU instruction
    # cpu.step() handles timers and interupts internally
    cycles = cpu.step()

    # Step PPU with the number of cycles taken by CPU
    ppu.step(cycles)

    # Handle inputs
    input_handler.handle_input(renderer.get_input())

```

For a more detailed explanation see my Blog Post [coming soon](anukindipa.github.io)

---


## Features

### Instruction-accurate CPU emulation
Implements the LR35902 instruction set with correct instruction semantics and timing at the instruction level.

### Memory-mapped I/O
Simulates the Game Boy memory layout, including ROM, RAM, VRAM, OAM, and memory-mapped registers.

### Timers and interrupts
Accurate handling of divider and timer registers, interrupt flags, and interrupt servicing logic.

### Scanline-based pixel rendering
Graphics output is generated using **line-by-line (scanline) rendering**, producing correct frame output without implementing a FIFO pixel pipeline.

### Performance optimisations
- Running under **PyPy** reduces render time from approximately 13 seconds to 1.5 seconds per 60 frames.
- Performance-critical components are being progressively rewritten in **C++** and exposed to Python using **pybind11**.

### Test ROM support
Includes [Blargg's CPU Test ROMs](https://github.com/retrio/gb-test-roms) for instruction validation and debugging.

---

## Getting Started

### Requirements

- Python 3.8+
- Optional (recommended for performance): **PyPy**

### Running

Clone the repository:

```bash
git clone https://github.com/anukindipa/gameboy-emulator.git
cd gameboy-emulator
```

Run using PyPy (Recommended):

```bash
pypy3 run.py
```

Run using CPython:

```bash
python3 run.py
```

## Limitations

- The emulator is not cycle-accurate.
- The PPU does not currently implement a FIFO-based pixel pipeline.
- Audio Processing Unit (APU) emulation is not yet implemented.
- Cartriage mapper support is limited.
- Some Components are completed but have not been uploaded to GitHub yet.
