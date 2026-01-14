"""functions that are used for opcodes with 0xCB prefix"""

def BIT_n_r8(cpu, bit, reg, HL=False):
    """
    Test bit n in register r8
    """
    if bit < 0 or bit > 7:
        raise ValueError("for BIT_n_r8 bit must be between 0 and 7")
    
    if HL:
        address = cpu.registers.HL
        value = cpu.read_d8(address)
    else:
        value = getattr(cpu.registers, reg)

    bit_value = (value >> bit) & 0x1

    cpu.registers.z_flag = int(bit_value == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 1

def RES_n_r8(cpu, bit, reg, HL=False):
    """
    Reset (set to 0) bit n in register r8
    uses bitwise AND ( & ) to reset bit using a mask
    the mask is created by negating (NOT) a left-shifted 1
    """
    if bit < 0 or bit > 7:
        raise ValueError("for RES_n_r8 bit must be between 0 and 7")

    mask = ~(1 << bit) & 0xFF

    if HL:
        address = cpu.registers.HL
        value = cpu.read_d8(address)
        new_value = value & mask
        cpu.write_d8(address, new_value)
    else:
        value = getattr(cpu.registers, reg)
        new_value = value & mask
        setattr(cpu.registers, reg, new_value)

def SET_n_r8(cpu, bit, reg, HL=False):
    """
    Set (set to 1) bit n in register r8
    uses bitwise OR ( | ) to set bit using a mask
    """
    if bit < 0 or bit > 7:
        raise ValueError("for SET_n_r8 bit must be between 0 and 7")

    mask = (1 << bit) & 0xFF

    if HL:
        address = cpu.registers.HL
        value = cpu.read_d8(address)
        new_value = value | mask
        cpu.write_d8(address, new_value)
    else:
        value = getattr(cpu.registers, reg)
        new_value = value | mask
        setattr(cpu.registers, reg, new_value)