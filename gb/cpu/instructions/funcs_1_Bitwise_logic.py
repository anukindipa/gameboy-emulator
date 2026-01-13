################################################################################
# Bitwise logic instructions
#    - AND, OR, XOR
################################################################################

def AND_A_r8(cpu, r_name, HL=False, d8 = False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    elif d8:
        r = cpu.read_d8()
    else:
        r = getattr(cpu.registers, r_name)

    a = cpu.registers.A
    res = a & r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 1
    cpu.registers.c_flag = 0

def OR_A_r8(cpu, r_name, HL=False, d8 = False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    elif d8:
        r = cpu.read_d8()
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a | r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0

def XOR_A_r8(cpu, r_name, HL=False, d8 = False):
    if HL:
        r = cpu.read_d8(cpu.registers.HL)
    elif d8:
        r = cpu.read_d8()
    else:
        r = getattr(cpu.registers, r_name)
    a = cpu.registers.A
    res = a ^ r

    cpu.registers.A = res & 0xff
    cpu.registers.z_flag = int(cpu.registers.A == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0
