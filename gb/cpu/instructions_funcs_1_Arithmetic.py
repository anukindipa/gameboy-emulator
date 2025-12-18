################################################################################
# 16 bit arithmetic instructions
#  - INC, DEC, ADD
################################################################################

def INC_r16(cpu, r_name):
    """16 bit register increments are not handled by the ALU.
    There is a seperate 16bit adder inside the sharp SM83,
    So INC_r16 does not affect flags"""
    val = getattr(cpu.registers, r_name)
    # wrap around
    val = (val+1) & 0xffff 
    setattr(cpu.registers, r_name, val)

def DEC_r16(cpu, r_name):
    val = getattr(cpu.registers, r_name)
    val = (val-1) % 0x10000 
    setattr(cpu.registers, r_name, val)

def ADD_HL_r16(cpu, r_name):
    # TODO: implement
    pass


################################################################################
# 8 bit arithmetic instructions
#   - ADD, INC, DEC, ADC, SUB, SBC, CP
################################################################################

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
