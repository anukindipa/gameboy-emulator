from gb.cpu.instructions.funcs_2 import *

def construct_cb_code_array():
    code_arr = [None] * 256
    regs = ['B', 'C', 'D', 'E', 'H', 'L', None, 'A']
    
    # 0x00 - 0x0F






    # The messy lambda usage is there because of `late binding` in python closures.
    # without passing bit_num = bit_num as a default argument to the lambda,
    # all the lambdas would use the last value of bit_num after the loop ends.
    # https://teachtimes.medium.com/late-binding-python-fe579b89a55e
    # https://realpython.com/python-closure/

    # 0x40 - 0x7F
    for i in range(0x40, 0x80):
        bit_num = (i - 0x40) // 8
        reg = regs[i % 8]
        if reg is None:
            code_arr[i] = lambda cpu, bit_num=bit_num: BIT_n_r8(cpu, bit_num, None, HL=True)
            # print(f"opcode {hex(i)}: BIT {bit_num}, (HL)")
        else:
            code_arr[i] =  lambda cpu, bit_num=bit_num, reg=reg: BIT_n_r8(cpu, bit_num, reg)
            # print(f"opcode {hex(i)}: BIT {bit_num}, {reg}")
    
    # 0x80 - 0xFF
    for i in range(0x80, 0xC0):
        bit_num = (i - 0x80) // 8
        reg = regs[i % 8]
        if reg is None:
            code_arr[i] = lambda cpu, bit_num=bit_num: RES_n_r8(cpu, bit_num, None, HL=True)
            # print(f"opcode {hex(i)}: RES {bit_num}, (HL)")
        else:
            code_arr[i] =  lambda cpu, bit_num=bit_num, reg=reg: RES_n_r8(cpu, bit_num, reg)
            # print(f"opcode {hex(i)}: RES {bit_num}, {reg}")

    for i in range(0xC0, 0x100):
        bit_num = (i - 0xC0) // 8
        reg = regs[i % 8]
        if reg is None:
            code_arr[i] = lambda cpu, bit_num=bit_num: SET_n_r8(cpu, bit_num, None, HL=True)
            # print(f"opcode {hex(i)}: SET {bit_num}, (HL)")
        else:
            code_arr[i] =  lambda cpu, bit_num=bit_num, reg=reg: SET_n_r8(cpu, bit_num, reg)
            # print(f"opcode {hex(i)}: SET {bit_num}, {reg}")
            

    return code_arr
