"""
Script to generate cycle count tables for unprefixed and CB prefixed opcodes.
The tables are saved in gb/cpu/instructions/cycle_arr_1.py and gb/cpu/instructions/cycle_arr_2.py respectively.
"""
import json

message_1  = """
cycle_arr_1 contains the cycle counts for unprefixed opcodes.
It is generated from the opcode data in gb/util/opcodes.json
using the script gb/util/generate_cycle_table.py\n"""
    
message_2  = """
cycle_arr_2 contains the cycle counts for CB prefixed opcodes.
It is generated from the opcode data in gb/util/opcodes.json
using the script gb/util/generate_cycle_table.py\n"""

def main():
    # Cycle data sourced from https://github.com/lmmendes/game-boy-opcodes (MIT License)
    # Original work by Luís Mendes
    with open('gb/util/opcodes.json', 'r') as f:
        cycle_data = json.load(f)
    
    unprefixed = {}
    for opcode_str in cycle_data['unprefixed'].items():
        cycles = opcode_str[1]["cycles"][0]
        print(f"Opcode: {opcode_str[0]}, Cycles: {cycles}")
        unprefixed[int(opcode_str[0], 16)] = cycles
    
    with open('gb/cpu/instructions/cycle_arr_1.py', 'w') as f:
        f.write(f'"""{message_1}"""\n\n')
        f.write("cycle_arr_1 = [\n")
        for i in range(256):
            f.write(f"    {unprefixed.get(i, 0):<2},  # 0x{i:02X}\n")
        f.write("]\n")
    
    prefixed = {}
    for opcode_str in cycle_data['cbprefixed'].items():
        cycles = opcode_str[1]["cycles"][0]
        print(f"Opcode: 0xCB {opcode_str[0]}, Cycles: {cycles}")
        prefixed[int(opcode_str[0], 16)] = cycles

    with open('gb/cpu/instructions/cycle_arr_2.py', 'w') as f:
        f.write(f'"""{message_2}"""\n\n')
        f.write("cycle_arr_2 = [\n")
        for i in range(256):
            f.write(f"    {prefixed.get(i, 0):>2},  # 0x{i:02X}\n")
        f.write("]\n")

if __name__ == "__main__":
    main()