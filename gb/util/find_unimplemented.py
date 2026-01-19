from gb.cpu.instructions.array_1 import construct_code_array
from gb.cpu.instructions.array_2 import construct_cb_code_array

code_array = construct_code_array()
code_array_2 = construct_cb_code_array()

with open("gb/boot/dmg_boot.gb", "rb") as f:
# with open("roms/tetris.gb", "rb") as f:
    # boot_rom = f.read(32768)
    boot_rom = f.read(256)

for i in range(256):
    print(f"{boot_rom[i]:02X}" , end=' ' if (i+1)%16 !=0 else '\n')


for i in range(256):
    op_code = boot_rom[i]
    if op_code == 0xCB:
        instruction = code_array_2[boot_rom[i + 1]]
        i += 1  # Skip next byte as it's part of CB instruction
        if instruction is None:
            print(f"Unimplemented instruction at byte {i:02X}: opcode 0xCB {boot_rom[i]:02X}")
    
    else:
        instruction = code_array[op_code]
        if instruction is None:
            print(f"Unimplemented instruction at byte {i:02X}: opcode {op_code:02X}")
    