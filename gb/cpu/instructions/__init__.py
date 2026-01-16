################################################################################
# Handles instruction of the sharp SM83 CPU
################################################################################


################################################################################
# behavior reference:
#   https://gbdev.io/pandocs/CPU_Instruction_Set.html
#   https://rgbds.gbdev.io/docs/v1.0.0/gbz80.7#POP_r16
#   https://gekkio.fi/files/gb-docs/gbctr.pdf
# optable:
#   https://gbdev.io/gb-opcodes/optables/
################################################################################


################################################################################
# for opcode mapping to functions see
#    - gb/cpu/instructions_array_1.py 
#    - gb/cpu/instructions_array_2.py
################################################################################
# for individual instruction implementations(non 0xCB prefixed) 
#    - gb/cpu/instructions_funcs_1_Arithmetic.py 
#    - gb/cpu/instructions_funcs_1_Bitwise_logic.py 
#    - gb/cpu/instructions_funcs_1_LD.py 
#    - gb/cpu/instructions_funcs_1_Misc.py 
#    - gb/cpu/instructions_funcs_1_Stack.py 
# 
# for individual instruction implementations(with 0xCB prefixed) 
#    - gb/cpu/instructions_funcs_2.py
################################################################################


# opcode mapping for normal opcodes 
from gb.cpu.instructions.array_1 import construct_code_array

# opcode mapping for 0xCB prefixed opcodes
from gb.cpu.instructions.array_2 import construct_cb_code_array

# cycle count tables
from gb.cpu.instructions.cycle_arr_1 import cycle_arr_1
from gb.cpu.instructions.cycle_arr_2 import cycle_arr_2

################################################################################
# code handler
################################################################################

class OP_Handler():
    __slots__ = ["code_arr", "cb_code_arr"]
    
    def __init__(self):
        self.code_arr = construct_code_array()
        self.cb_code_arr = construct_cb_code_array()

    def run_code(self, cpu, code_num):
        fn = self.code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode {hex(code_num)} is not implemented.\n\
                    Program Counter at: {cpu.registers.PC-1:04x}")
        fn(cpu)

    def run_cb_code(self, cpu, code_num):
        fn = self.cb_code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode 0xCB, {hex(code_num)} is not implemented")
        fn(cpu)

    def execute_opcode(self, cpu, opcode):
        if opcode is None:
            raise ValueError("opcode is None")
        if opcode==0xcb:
            cb_opcode = cpu.read_d8()
            self.run_cb_code(cpu, cb_opcode)
            # +4 for the CB prefix fetch
            cycles = cycle_arr_2[cb_opcode] + 4  
            print(f"Opcode 0xCB {hex(cb_opcode):4} took {cycles:-2} cycles.", end=' ')
            return cycles

        else:
            self.run_code(cpu, opcode)
            cycles = cycle_arr_1[opcode]
            print(f"Opcode {hex(opcode):9} took {cycles:-2} cycles.", end=' ')
            return cycles
