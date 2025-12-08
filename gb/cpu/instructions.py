"""
r8 is a normal register like A, B
r16 is a 'pair' register like DE, HL

d16 is a 16 bit value
"""

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

def INC_r8(cpu, r_name):
    val = getattr(cpu.registers, r_name)
    val = (val+1) & 0xff 
    setattr(cpu.registers, r_name, val)
    cpu.registers.z_flag = int(val==0)
    cpu.registers.n_flag = 0
    # fine for inc but h_flag must be calculated differently for other ops
    cpu.registers.h_flag = int(val&0xf == 0)

def DEC_r8(cpu, r_name):
    val = getattr(cpu.registers, r_name)
    val = (val-1) % 0xff
    setattr(cpu.registers, r_name, val)
    cpu.registers.z_flag = int(val==0)
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = int(val&0xf == 0xf)

def DEC_r16(cpu, r_name):
    val = getattr(cpu.registers, r_name)
    val = (val-1) % 0xffff 
    setattr(cpu.registers, r_name, val)


class OP_Handler():
    __slots__ = ["code_arr", "cb_code_arr"]
    
    def __init__(self):
        self.code_arr = [None] * 256

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

    def run_code(self, cpu, code_num):
        fn = self.code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode {code_num} is not implemented")
        fn(cpu)

    def run_cb_code(self, cpu, code_num):
        fn = self.cb_code_arr[code_num]
        if fn==None:
            raise NotImplementedError(f"opcode 0xCB, {code_num} is not implemented")
        fn(cpu)
