################################################################################
# Handles instruction of the sharp SM83 CPU
################################################################################
# behavior reference:
#   https://gbdev.io/pandocs/CPU_Instruction_Set.html
#   https://rgbds.gbdev.io/docs/v1.0.0/gbz80.7#POP_r16
# optable:
#   https://gbdev.io/gb-opcodes/optables/
################################################################################
# r8 is a normal register like A, B
# r16 is a 'pair' register like DE, HL
# d16 is a 16 bit value
################################################################################

def NOP(cpu):
    pass

def LD_r16_d16(cpu, r_name):
    d16 = cpu.read_d16()
    setattr(cpu.registers, r_name, d16)
    
def LD_r8_r8(cpu, r1_name, r2_name):
    val = getattr(cpu.registers, r2_name)
    setattr(cpu.registers, r1_name, val)
    
def LD_r8_d8(cpu, r_name):
    d8 = cpu.read_d8()
    setattr(cpu.registers, r_name, d8)

def INC_r16(cpu, r_name):
    """16 bit register increments are not handled by the ALU.
    There is a seperate 16bit adder inside the sharp SM83,
    So INC_r16 does not affect flags"""
    val = getattr(cpu.registers, r_name)
    # wrap around
    val = (val+1) & 0xffff 
    setattr(cpu.registers, r_name, val)

def INC_r8(cpu, r_name, HL=False):
    if HL:
        # TODO: check if behavior is correct
        addr = cpu.registers.HL
        val = cpu.read_d8(addr)
        val = (val+1) & 0xff
        cpu.write_d8(addr, val)
    else:
        val = getattr(cpu.registers, r_name)
        val = (val+1) & 0xff 
        setattr(cpu.registers, r_name, val)
    cpu.registers.z_flag = int(val==0)
    cpu.registers.n_flag = 0
    # fine for inc but h_flag must be calculated differently for other ops
    cpu.registers.h_flag = int(val&0xf == 0)

def DEC_r8(cpu, r_name, HL=False):
    if HL:
        # TODO: check if behavior is correct
        addr = cpu.registers.HL
        val = cpu.read_d8(addr)
        val = (val-1) % 0x100
        cpu.write_d8(addr, val)
    else:
        val = getattr(cpu.registers, r_name)
        val = (val-1) % 0x100
        setattr(cpu.registers, r_name, val)
    cpu.registers.z_flag = int(val==0)
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = int(val&0xf == 0xf)

def DEC_r16(cpu, r_name):
    val = getattr(cpu.registers, r_name)
    val = (val-1) % 0x10000 
    setattr(cpu.registers, r_name, val)

def ADD_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a + r

    cpu.registers.z_flag = int((res & 0xff) == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = int(a + r > 0xf)
    cpu.registers.c_flag = int(res > 0xff)

    cpu.registers.A = res & 0xff

def ADC_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    c = cpu.registers.c_flag
    res = a + r + c

    cpu.registers.z_flag = int((res & 0xff) == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = int((a & 0xf) + (r & 0xf) + c > 0xf)
    cpu.registers.c_flag = int(res > 0xff)

    cpu.registers.A = res & 0xff

def SUB_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a - r

    # %0x100 is used just in case
    cpu.registers.z_flag = int((res%0x100) == 0)
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = int(r%0x10 > a%0x10)
    cpu.registers.c_flag = int(r > a)

    cpu.registers.A = res % 0x100

def SBC_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    c = cpu.registers.c_flag
    res = a - (r + c)

    cpu.registers.z_flag = int((res%0x100) == 0)
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = int(((r+c) % 0xf) > (a%0xf))
    cpu.registers.c_flag = int(r + c > a)

    cpu.registers.A = res % 0x100

def AND_A_r8(cpu, r_name):
    r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a & r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 1
    cpu.registers.c_flag = 0

def OR_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a | r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0

def XOR_A_r8(cpu, r_name, HL=False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a ^ r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0

def CP_A_r8(cpu, r_name, HL=False):
    """
    compare (not copy) r8 to A. Done by subtracting r8 from A and setting flags.
    result is discarded
    """
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a - r

    cpu.registers.z_flag = int((res%0x100) == 0)
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = int((r%0x10) > (a%0x10))
    cpu.registers.c_flag = int(r > a)

class OP_Handler():
    __slots__ = ["code_arr", "cb_code_arr"]
    
    def __init__(self):
        self.code_arr: list = [None] * 256

        # 0x00..0x0f
        self.code_arr[0x00] = NOP
        self.code_arr[0x01] = lambda cpu: LD_r16_d16(cpu, "BC")
        #
        self.code_arr[0x03] = lambda cpu: INC_r16(cpu, "BC")
        self.code_arr[0x04] = lambda cpu: INC_r8(cpu, "B")
        self.code_arr[0x05] = lambda cpu: DEC_r8(cpu, "B")
        self.code_arr[0x06] = lambda cpu: LD_r8_d8(cpu, "B")
        #
        #
        self.code_arr[0x0b] = lambda cpu: DEC_r16(cpu, "BC")
        self.code_arr[0x0c] = lambda cpu: INC_r8(cpu, "C")
        self.code_arr[0x0d] = lambda cpu: DEC_r8(cpu, "C")
        self.code_arr[0x0e] = lambda cpu: LD_r8_d8(cpu, "C")
        #

        # 0x10..0x1f
        self.code_arr[0x11] = lambda cpu: LD_r16_d16(cpu, "DE")
        #
        self.code_arr[0x13] = lambda cpu: INC_r16(cpu, "DE")
        self.code_arr[0x14] = lambda cpu: INC_r8(cpu, "D")
        self.code_arr[0x15] = lambda cpu: DEC_r8(cpu, "D")
        self.code_arr[0x16] = lambda cpu: LD_r8_d8(cpu, "D")
        #
        #
        self.code_arr[0x1b] = lambda cpu: DEC_r16(cpu, "DE")
        self.code_arr[0x1c] = lambda cpu: INC_r8(cpu, "E")
        self.code_arr[0x1d] = lambda cpu: DEC_r8(cpu, "E")
        self.code_arr[0x1e] = lambda cpu: LD_r8_d8(cpu, "E")
        #
    
        # 0x20..0x2f
        self.code_arr[0x21] = lambda cpu: LD_r16_d16(cpu, "HL")
        # 
        self.code_arr[0x23] = lambda cpu: INC_r16(cpu, "HL")
        self.code_arr[0x24] = lambda cpu: INC_r8(cpu, "H")
        self.code_arr[0x25] = lambda cpu: DEC_r8(cpu, "H")
        self.code_arr[0x26] = lambda cpu: LD_r8_d8(cpu, "H")
        #
        #
        self.code_arr[0x2b] = lambda cpu: DEC_r16(cpu, "HL")
        self.code_arr[0x2c] = lambda cpu: INC_r8(cpu, "L")
        self.code_arr[0x2d] = lambda cpu: DEC_r8(cpu, "L")
        self.code_arr[0x2e] = lambda cpu: LD_r8_d8(cpu, "L")
        #

        # 0x30..0x3f
        self.code_arr[0x31] = lambda cpu: LD_r16_d16(cpu, "SP")
        # 
        self.code_arr[0x33] = lambda cpu: INC_r16(cpu, "SP")
        self.code_arr[0x34] = lambda cpu: INC_r8(cpu, None, HL=True)
        self.code_arr[0x35] = lambda cpu: DEC_r8(cpu, None, HL=True)
        #
        #
        self.code_arr[0x3b] = lambda cpu: DEC_r16(cpu, "SP")
        self.code_arr[0x3c] = lambda cpu: INC_r8(cpu, "A")
        self.code_arr[0x3d] = lambda cpu: DEC_r8(cpu, "A")
        self.code_arr[0x3e] = lambda cpu: LD_r8_d8(cpu, "A")
        #
        
        # 0x40..0x4f
        self.code_arr[0x40] = lambda cpu: LD_r8_r8(cpu, "B", "B")
        self.code_arr[0x41] = lambda cpu: LD_r8_r8(cpu, "B", "C")
        self.code_arr[0x42] = lambda cpu: LD_r8_r8(cpu, "B", "D")
        self.code_arr[0x43] = lambda cpu: LD_r8_r8(cpu, "B", "E")
        self.code_arr[0x44] = lambda cpu: LD_r8_r8(cpu, "B", "H")
        self.code_arr[0x45] = lambda cpu: LD_r8_r8(cpu, "B", "L")
        #
        self.code_arr[0x47] = lambda cpu: LD_r8_r8(cpu, "B", "A")
        self.code_arr[0x48] = lambda cpu: LD_r8_r8(cpu, "C", "B")
        self.code_arr[0x49] = lambda cpu: LD_r8_r8(cpu, "C", "C")
        self.code_arr[0x4a] = lambda cpu: LD_r8_r8(cpu, "C", "D")
        self.code_arr[0x4b] = lambda cpu: LD_r8_r8(cpu, "C", "E")
        self.code_arr[0x4c] = lambda cpu: LD_r8_r8(cpu, "C", "H")
        self.code_arr[0x4d] = lambda cpu: LD_r8_r8(cpu, "C", "L")
        #
        self.code_arr[0x4f] = lambda cpu: LD_r8_r8(cpu, "C", "A")

        # 0x50..0x5f
        self.code_arr[0x50] = lambda cpu: LD_r8_r8(cpu, "D", "B")
        self.code_arr[0x51] = lambda cpu: LD_r8_r8(cpu, "D", "C")
        self.code_arr[0x52] = lambda cpu: LD_r8_r8(cpu, "D", "D")
        self.code_arr[0x53] = lambda cpu: LD_r8_r8(cpu, "D", "E")
        self.code_arr[0x54] = lambda cpu: LD_r8_r8(cpu, "D", "H")
        self.code_arr[0x55] = lambda cpu: LD_r8_r8(cpu, "D", "L")
        #
        self.code_arr[0x57] = lambda cpu: LD_r8_r8(cpu, "D", "A")
        self.code_arr[0x58] = lambda cpu: LD_r8_r8(cpu, "E", "B")
        self.code_arr[0x59] = lambda cpu: LD_r8_r8(cpu, "E", "C")
        self.code_arr[0x5a] = lambda cpu: LD_r8_r8(cpu, "E", "D")
        self.code_arr[0x5b] = lambda cpu: LD_r8_r8(cpu, "E", "E")
        self.code_arr[0x5c] = lambda cpu: LD_r8_r8(cpu, "E", "H")
        self.code_arr[0x5d] = lambda cpu: LD_r8_r8(cpu, "E", "L")
        #
        self.code_arr[0x5f] = lambda cpu: LD_r8_r8(cpu, "E", "A")

        # 0x60..0x6f
        self.code_arr[0x60] = lambda cpu: LD_r8_r8(cpu, "H", "B")
        self.code_arr[0x61] = lambda cpu: LD_r8_r8(cpu, "H", "C")
        self.code_arr[0x62] = lambda cpu: LD_r8_r8(cpu, "H", "D")
        self.code_arr[0x63] = lambda cpu: LD_r8_r8(cpu, "H", "E")
        self.code_arr[0x64] = lambda cpu: LD_r8_r8(cpu, "H", "H")
        self.code_arr[0x65] = lambda cpu: LD_r8_r8(cpu, "H", "L")
        #
        self.code_arr[0x67] = lambda cpu: LD_r8_r8(cpu, "H", "A")
        self.code_arr[0x68] = lambda cpu: LD_r8_r8(cpu, "L", "B")
        self.code_arr[0x69] = lambda cpu: LD_r8_r8(cpu, "L", "C")
        self.code_arr[0x6a] = lambda cpu: LD_r8_r8(cpu, "L", "D")
        self.code_arr[0x6b] = lambda cpu: LD_r8_r8(cpu, "L", "E")
        self.code_arr[0x6c] = lambda cpu: LD_r8_r8(cpu, "L", "H")
        self.code_arr[0x6d] = lambda cpu: LD_r8_r8(cpu, "L", "L")
        #
        self.code_arr[0x6f] = lambda cpu: LD_r8_r8(cpu, "L", "A")

        # 0x70..0x7f
        #
        #
        self.code_arr[0x78] = lambda cpu: LD_r8_r8(cpu, "A", "B")
        self.code_arr[0x79] = lambda cpu: LD_r8_r8(cpu, "A", "C")
        self.code_arr[0x7a] = lambda cpu: LD_r8_r8(cpu, "A", "D")
        self.code_arr[0x7b] = lambda cpu: LD_r8_r8(cpu, "A", "E")
        self.code_arr[0x7c] = lambda cpu: LD_r8_r8(cpu, "A", "H")
        self.code_arr[0x7d] = lambda cpu: LD_r8_r8(cpu, "A", "L")
        #
        self.code_arr[0x7f] = lambda cpu: LD_r8_r8(cpu, "A", "A")
        
        # 0x80..0x8f 
        self.code_arr[0x80] = lambda cpu: ADD_A_r8(cpu, "B")
        self.code_arr[0x81] = lambda cpu: ADD_A_r8(cpu, "C")
        self.code_arr[0x82] = lambda cpu: ADD_A_r8(cpu, "D")
        self.code_arr[0x83] = lambda cpu: ADD_A_r8(cpu, "E")
        self.code_arr[0x84] = lambda cpu: ADD_A_r8(cpu, "H")
        self.code_arr[0x85] = lambda cpu: ADD_A_r8(cpu, "L")
        self.code_arr[0x86] = lambda cpu: ADD_A_r8(cpu, None, HL=True)
        self.code_arr[0x87] = lambda cpu: ADD_A_r8(cpu, "A")
        self.code_arr[0x88] = lambda cpu: ADC_A_r8(cpu, "B")
        self.code_arr[0x89] = lambda cpu: ADC_A_r8(cpu, "C")
        self.code_arr[0x8a] = lambda cpu: ADC_A_r8(cpu, "D")
        self.code_arr[0x8b] = lambda cpu: ADC_A_r8(cpu, "E")
        self.code_arr[0x8c] = lambda cpu: ADC_A_r8(cpu, "H")
        self.code_arr[0x8d] = lambda cpu: ADC_A_r8(cpu, "L")
        self.code_arr[0x8e] = lambda cpu: ADC_A_r8(cpu, None, HL=True)
        self.code_arr[0x8f] = lambda cpu: ADC_A_r8(cpu, "A")
        
        # 0x90..0x9f 
        self.code_arr[0x90] = lambda cpu: SUB_A_r8(cpu, "B")
        self.code_arr[0x91] = lambda cpu: SUB_A_r8(cpu, "C")
        self.code_arr[0x92] = lambda cpu: SUB_A_r8(cpu, "D")
        self.code_arr[0x93] = lambda cpu: SUB_A_r8(cpu, "E")
        self.code_arr[0x94] = lambda cpu: SUB_A_r8(cpu, "H")
        self.code_arr[0x95] = lambda cpu: SUB_A_r8(cpu, "L")
        self.code_arr[0x96] = lambda cpu: SUB_A_r8(cpu, None, HL=True)
        self.code_arr[0x97] = lambda cpu: SUB_A_r8(cpu, "A")
        self.code_arr[0x98] = lambda cpu: SBC_A_r8(cpu, "B")
        self.code_arr[0x99] = lambda cpu: SBC_A_r8(cpu, "C")
        self.code_arr[0x9a] = lambda cpu: SBC_A_r8(cpu, "D")
        self.code_arr[0x9b] = lambda cpu: SBC_A_r8(cpu, "E")
        self.code_arr[0x9c] = lambda cpu: SBC_A_r8(cpu, "H")
        self.code_arr[0x9d] = lambda cpu: SBC_A_r8(cpu, "L")
        self.code_arr[0x9d] = lambda cpu: SBC_A_r8(cpu, None, HL=True)
        self.code_arr[0x9f] = lambda cpu: SBC_A_r8(cpu, "A")

        # 0xa0..0xaf 
        self.code_arr[0xa0] = lambda cpu: AND_A_r8(cpu, "B")
        self.code_arr[0xa1] = lambda cpu: AND_A_r8(cpu, "C")
        self.code_arr[0xa2] = lambda cpu: AND_A_r8(cpu, "D")
        self.code_arr[0xa3] = lambda cpu: AND_A_r8(cpu, "E")
        self.code_arr[0xa4] = lambda cpu: AND_A_r8(cpu, "H")
        self.code_arr[0xa5] = lambda cpu: AND_A_r8(cpu, "L")
        self.code_arr[0xa6] = lambda cpu: AND_A_r8(cpu, None, HL=True)
        self.code_arr[0xa7] = lambda cpu: AND_A_r8(cpu, "A")
        self.code_arr[0xa8] = lambda cpu: XOR_A_r8(cpu, "B")
        self.code_arr[0xa9] = lambda cpu: XOR_A_r8(cpu, "C")
        self.code_arr[0xaa] = lambda cpu: XOR_A_r8(cpu, "D")
        self.code_arr[0xab] = lambda cpu: XOR_A_r8(cpu, "E")
        self.code_arr[0xac] = lambda cpu: XOR_A_r8(cpu, "H")
        self.code_arr[0xad] = lambda cpu: XOR_A_r8(cpu, "L")
        self.code_arr[0xae] = lambda cpu: XOR_A_r8(cpu, None, HL=True)
        self.code_arr[0xaf] = lambda cpu: XOR_A_r8(cpu, "A")

        # 0xb0..0xbf 
        self.code_arr[0xb0] = lambda cpu: OR_A_r8(cpu, "B")
        self.code_arr[0xb1] = lambda cpu: OR_A_r8(cpu, "C")
        self.code_arr[0xb2] = lambda cpu: OR_A_r8(cpu, "D")
        self.code_arr[0xb3] = lambda cpu: OR_A_r8(cpu, "E")
        self.code_arr[0xb4] = lambda cpu: OR_A_r8(cpu, "H")
        self.code_arr[0xb5] = lambda cpu: OR_A_r8(cpu, "L")
        self.code_arr[0xb6] = lambda cpu: OR_A_r8(cpu, None, HL=True)
        self.code_arr[0xb7] = lambda cpu: OR_A_r8(cpu, "A")
        self.code_arr[0xb8] = lambda cpu: CP_A_r8(cpu, "B")
        self.code_arr[0xb9] = lambda cpu: CP_A_r8(cpu, "C")
        self.code_arr[0xba] = lambda cpu: CP_A_r8(cpu, "D")
        self.code_arr[0xbb] = lambda cpu: CP_A_r8(cpu, "E")
        self.code_arr[0xbc] = lambda cpu: CP_A_r8(cpu, "H")
        self.code_arr[0xbd] = lambda cpu: CP_A_r8(cpu, "L")
        self.code_arr[0xbe] = lambda cpu: CP_A_r8(cpu, None, HL=True)
        self.code_arr[0xbf] = lambda cpu: CP_A_r8(cpu, "A")

    def run_code(self, cpu, code_num):
        fn = self.code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode {code_num} is not implemented.\n\
                    Program Counter at: {cpu.registers.PC-1:04x}")
        fn(cpu)

    def run_cb_code(self, cpu, code_num):
        fn = self.cb_code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode 0xCB, {code_num} is not implemented")
        fn(cpu)
