"""Bit operation instructions (rotate, shift)"""

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
