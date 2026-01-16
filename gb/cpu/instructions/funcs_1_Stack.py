from gb.util.bit_ops import d8_to_s8

def CALL_cc_d16(cpu, condition=True):
    """
    if condition is True, Push address of next instruction to stack and jump to
    immediate 16-bit address.
    """
    lsb = cpu.read_d8()
    msb = cpu.read_d8()
    PC_after = (msb << 8) | lsb

    if not condition:
        return

    # save current PC to stack
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC >> 8) & 0xFF)
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC) & 0xFF)

    # jump to immediate address
    cpu.registers.PC = PC_after

def PUSH_r16(cpu, reg):
    r_val = getattr(cpu.registers, reg)
    lsb = r_val & 0xFF
    msb = (r_val >> 8) & 0xFF
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, msb)
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, lsb)

def POP_r16(cpu, reg):
    # read from stack in LSB then MSB order
    lsb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    msb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    
    # write the 2 bytes to the register
    r_val = (msb << 8) | lsb
    setattr(cpu.registers, reg, r_val)

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
    if ((cpu.registers.SP & 0x0F) + (value & 0x0F)) > 0x0F:
        cpu.registers.h_flag = 1
    else:
        cpu.registers.h_flag = 0

    # check overflow for the 7th bit
    if ((cpu.registers.SP & 0xFF) + value) > 0xFF:
        cpu.registers.c_flag = 1
    else:
        cpu.registers.c_flag = 0

    cpu.registers.SP = (cpu.registers.SP + d8_to_s8(value)) & 0xFFFF

def LD_d16_SP(cpu):
    """
    Read 16-bit immediate address and store SP there.
    for instruction 0x08.
    """
    address = cpu.read_d16()
    SP = cpu.registers.SP
    cpu.write_d8(address, SP & 0xFF)
    # bitwise rightshift same as dividing by 2^8
    cpu.write_d8(address + 1, (SP >> 8) & 0xFF)

    
def LD_SP_HL(cpu):
    """
    Load SP with the value in HL.
    for instruction 0xF9.
    """
    cpu.registers.SP = cpu.registers.HL

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
    if ((cpu.registers.SP & 0x0F) + (value & 0x0F)) > 0x0F:
        cpu.registers.h_flag = 1
    else:
        cpu.registers.h_flag = 0

    # check overflow for the 7th bit
    if ((cpu.registers.SP & 0xFF) + value) > 0xFF:
        cpu.registers.c_flag = 1
    else:
        cpu.registers.c_flag = 0

    cpu.registers.HL = (cpu.registers.SP + d8_to_s8(value)) & 0xFFFF