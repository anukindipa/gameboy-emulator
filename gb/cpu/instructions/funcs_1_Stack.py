from gb.util.bit_ops import d8_to_s8

def ADD_SP_s8(cpu):
    """
    Add signed 8-bit immediate value to SP.
    for instruction 0xE8.
    """
    value = cpu.read_d8()
    
    # Set flags
    cpu.registers.z_flag = 0
    cpu.registers.n_flag = 0

    # overflow for the 3rd bit
    if ((cpu.registers.sp & 0x0F) + (value & 0x0F)) > 0x0F:
        cpu.registers.h_flag = 1
    else:
        cpu.registers.h_flag = 0

    # check overflow for the 7th bit
    if ((cpu.registers.sp & 0xFF) + value) > 0xFF:
        cpu.registers.c_flag = 1
    else:
        cpu.registers.c_flag = 0

    cpu.registers.sp = (cpu.registers.sp + d8_to_s8(value)) & 0xFFFF
    
def LD_SP_HL(cpu):
    """
    Load SP with the value in HL.
    for instruction 0xF9.
    """
    cpu.registers.sp = cpu.registers.HL

def LD_HL_SP_plus_s8(cpu):
    """
    Load HL with SP plus signed 8-bit immediate value.
    for instruction 0xF8.
    """
    value = cpu.read_d8()
    
    # Set flags
    cpu.registers.z_flag = 0
    cpu.registers.n_flag = 0

    # overflow for the 3rd bit
    if ((cpu.registers.sp & 0x0F) + (value & 0x0F)) > 0x0F:
        cpu.registers.h_flag = 1
    else:
        cpu.registers.h_flag = 0

    # check overflow for the 7th bit
    if ((cpu.registers.sp & 0xFF) + value) > 0xFF:
        cpu.registers.c_flag = 1
    else:
        cpu.registers.c_flag = 0

    cpu.registers.HL = (cpu.registers.sp + d8_to_s8(value)) & 0xFFFF