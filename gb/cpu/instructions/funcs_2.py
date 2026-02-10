"""functions that are used for opcodes with 0xCB prefix"""

def RL_r8(cpu, reg, HL=False):
    """
    Rotate register left through carry (0x17).
    Old bit 7 goes to carry, carry goes to bit 0.
    RL A is Like RLA (0x17), but behavior is different:
    z_flag is set according to result.
    https://gekkio.fi/files/gb-docs/gbctr.pdf (page 84-RLA, RL r8-92)
    """
    val = getattr(cpu.registers, reg) if not HL else cpu.read_d8(cpu.registers.HL)
    bit_7 = (val >> 7) & 0x1
    val = val << 1 | cpu.registers.c_flag
    val &= 0xFF  # keep it to 8 bits
    
    # Write result back
    if HL:
        cpu.write_d8(cpu.registers.HL, val)
    else:
        setattr(cpu.registers, reg, val)
    
    # Set flags
    cpu.registers.z_flag = int(val == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_7
    
def RR_r8(cpu, reg, HL=False):
    """
    Rotate register right through carry (0x1F).
    Old bit 0 goes to carry, carry goes to bit 7.
    https://gekkio.fi/files/gb-docs/gbctr.pdf (page 84-RRA, RR r8-92)
    """
    val = getattr(cpu.registers, reg) if not HL else cpu.read_d8(cpu.registers.HL)
    bit_0 = val & 0x1
    val = (val >> 1) | ((cpu.registers.c_flag << 7) & 0x80)
    
    # Write result back
    if HL:
        cpu.write_d8(cpu.registers.HL, val)
    else:
        setattr(cpu.registers, reg, val)
    
    # Set flags
    cpu.registers.z_flag = int(val == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_0

def SLA_r8(cpu, reg, HL=False):
    """
    Shifts the 8-bit register r value left by one bit using an arithmetic shift.
    """
    if HL:
        val = cpu.read_d8(cpu.registers.HL)
    else:
        val = getattr(cpu.registers, reg)
    
    bit_7 = (val >> 7) & 0x1
    val = ((val << 1) & 0xFF)
    
    # write back
    if HL:
        cpu.write_d8(cpu.registers.HL, val)
    else:
        setattr(cpu.registers, reg, val)

    cpu.registers.z_flag = int(val == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_7

def SWAP_r8(cpu, reg, HL=False):
    """
    shift lower nibble to upper nibble and upper nibble to lower nibble.
    set z flag if result is zero.
    """
    if HL:
        val = cpu.read_d8(cpu.registers.HL)
        lower_nibble = val & 0x0F
        upper_nibble = (val >> 4) & 0x0F
        val = (lower_nibble << 4) | upper_nibble
        cpu.write_d8(cpu.registers.HL, val)
    else:
        val = getattr(cpu.registers, reg)
        lower_nibble = val & 0x0F
        upper_nibble = (val >> 4) & 0x0F
        val = (lower_nibble << 4) | upper_nibble
        setattr(cpu.registers, reg, val)
    
    cpu.registers.z_flag = int(val == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0
    
def SRL_r8(cpu, reg, HL=False):
    """
    Shifts the 8-bit register r value right by one bit using a logical shift.
    """
    if HL:
        val = cpu.read_d8(cpu.registers.HL)
    else:
        val = getattr(cpu.registers, reg)
    
    bit_0 = val & 0x1
    val = (val >> 1) & 0xFF

    # write back
    if HL:
        cpu.write_d8(cpu.registers.HL, val)
    else:
        setattr(cpu.registers, reg, val)
        
    cpu.registers.z_flag = int(val == 0)
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_0
    

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
