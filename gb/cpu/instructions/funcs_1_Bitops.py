"""Bit operation instructions (rotate, shift)"""

def RRA(cpu):
    """
    Used in 0x1f.
    Rotate A right. Old bit 0 to carry and bit 7.
    https://gekkio.fi/files/gb-docs/gbctr.pdf (page 84-RRA)
    """
    value = cpu.registers.A
    bit_0 = value & 0x1
    result = ((value >> 1) | (bit_0 << 7)) & 0xFF
    
    cpu.registers.A = result
    
    cpu.registers.z_flag = 0  # Always 0 for RRA
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_0

def RLCA(cpu):
    """
    Used in 0x07.
    Rotate A left. Old bit 7 to carry and bit 0.
    https://gekkio.fi/files/gb-docs/gbctr.pdf (page 84-RLCA)
    """
    value = cpu.registers.A
    bit_7 = (value >> 7) & 0x1
    result = ((value << 1) | bit_7) & 0xFF
    
    cpu.registers.A = result
    
    cpu.registers.z_flag = 0  # Always 0 for RLCA
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = bit_7

def RLA(cpu):
    """
    Used in 0x17.
    Rotate A left through carry.
    Old bit 7 goes to carry, carry goes to bit 0.
    RL A is Like RLA (0x17), but behavior is different:
    Z flag is always 0.
    https://gekkio.fi/files/gb-docs/gbctr.pdf (page 84-RLA, RL r8-92)
    """
    value = cpu.registers.A
    old_carry = cpu.registers.c_flag
    new_carry = (value >> 7) & 0x1
    
    result = ((value << 1) | old_carry) & 0xFF
    
    cpu.registers.A = result
    
    cpu.registers.z_flag = 0  # Always 0 for RLA
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = new_carry
