from gb.cpu.instructions.funcs_2 import *

def construct_cb_code_array():
    code_arr = [None] * 256
    regs = ['B', 'C', 'D', 'E', 'H', 'L', None, 'A']
    
    # 0x00 - 0x0F
    code_arr[0x10] = lambda cpu: RL_r8(cpu, 'B')
    code_arr[0x11] = lambda cpu: RL_r8(cpu, 'C')
    code_arr[0x12] = lambda cpu: RL_r8(cpu, 'D')
    code_arr[0x13] = lambda cpu: RL_r8(cpu, 'E')
    code_arr[0x14] = lambda cpu: RL_r8(cpu, 'H')
    code_arr[0x15] = lambda cpu: RL_r8(cpu, 'L')
    code_arr[0x16] = lambda cpu: RL_r8(cpu, None, HL=True)
    code_arr[0x17] = lambda cpu: RL_r8(cpu, 'A')
    code_arr[0x18] = lambda cpu: RR_r8(cpu, 'B')
    code_arr[0x19] = lambda cpu: RR_r8(cpu, 'C')
    code_arr[0x1a] = lambda cpu: RR_r8(cpu, 'D')
    code_arr[0x1b] = lambda cpu: RR_r8(cpu, 'E')
    code_arr[0x1c] = lambda cpu: RR_r8(cpu, 'H')
    code_arr[0x1d] = lambda cpu: RR_r8(cpu, 'L')
    code_arr[0x1e] = lambda cpu: RR_r8(cpu, None, HL=True)
    code_arr[0x1f] = lambda cpu: RR_r8(cpu, 'A')

    # 0x20 - 0x2F
    code_arr[0x20] = lambda cpu: SLA_r8(cpu, 'B')
    code_arr[0x21] = lambda cpu: SLA_r8(cpu, 'C')
    code_arr[0x22] = lambda cpu: SLA_r8(cpu, 'D')
    code_arr[0x23] = lambda cpu: SLA_r8(cpu, 'E')
    code_arr[0x24] = lambda cpu: SLA_r8(cpu, 'H')
    code_arr[0x25] = lambda cpu: SLA_r8(cpu, 'L')
    code_arr[0x26] = lambda cpu: SLA_r8(cpu, None, HL=True)
    code_arr[0x27] = lambda cpu: SLA_r8(cpu, 'A')

    # 0x30 - 0x3F
    code_arr[0x30] = lambda cpu: SWAP_r8(cpu, 'B')
    code_arr[0x31] = lambda cpu: SWAP_r8(cpu, 'C')
    code_arr[0x32] = lambda cpu: SWAP_r8(cpu, 'D')
    code_arr[0x33] = lambda cpu: SWAP_r8(cpu, 'E')
    code_arr[0x34] = lambda cpu: SWAP_r8(cpu, 'H')
    code_arr[0x35] = lambda cpu: SWAP_r8(cpu, 'L')
    code_arr[0x36] = lambda cpu: SWAP_r8(cpu, None, HL=True)
    code_arr[0x37] = lambda cpu: SWAP_r8(cpu, 'A')
    code_arr[0x38] = lambda cpu: SRL_r8(cpu, 'B')
    code_arr[0x39] = lambda cpu: SRL_r8(cpu, 'C')
    code_arr[0x3a] = lambda cpu: SRL_r8(cpu, 'D')
    code_arr[0x3b] = lambda cpu: SRL_r8(cpu, 'E')
    code_arr[0x3c] = lambda cpu: SRL_r8(cpu, 'H')
    code_arr[0x3d] = lambda cpu: SRL_r8(cpu, 'L')
    code_arr[0x3e] = lambda cpu: SRL_r8(cpu, None, HL=True)
    code_arr[0x3f] = lambda cpu: SRL_r8(cpu, 'A')



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
    
    # 0x80 - 0xBF
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
