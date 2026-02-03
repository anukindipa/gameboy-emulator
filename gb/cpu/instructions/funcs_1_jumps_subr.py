"""Jumps and subroutine instructions"""

def JR_cc_s8(cpu, condition):
    """Jump relative by signed s8 if condition is True"""
    # PC is incremented regardless of condition
    offset = cpu.read_s8()

    if not condition:
        return

    # adding is correct as PC is incremented once reading opcode 
    # and again after reading d8:
    # https://www.reddit.com/r/EmuDev/comments/jmo5x1/gameboy_0x20_instruction/
    cpu.registers.PC = (cpu.registers.PC + offset) & 0xFFFF
    
def JP_HL(cpu):
    """Jump to address in HL register"""
    cpu.registers.PC = cpu.registers.HL
    
def JP_cc_d16(cpu, condition):
    """Jump to immediate 16-bit address if condition is True"""
    # PC is incremented regardless of condition
    lsb = cpu.read_d8()
    msb = cpu.read_d8()
    address = (msb << 8) | lsb

    if not condition:
        return

    cpu.registers.PC = address

def RET_cc(cpu, condition=True):
    """Return from subroutine if condition is True"""
    if not condition:
        return
    # Restore PC from stack
    lsb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    msb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    
    # Set PC to the address popped from stack
    cpu.registers.PC = (msb << 8) | lsb

def CALL_cc_d16(cpu, condition):
    """
    if condition is True, Push address of next instruction to stack and jump to
    immediate 16-bit address.
    """
    lsb = cpu.read_d8()
    msb = cpu.read_d8()
    d16 = (msb << 8) | lsb

    if not condition:
        return

    # save current PC to stack (push PC onto stack)
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC >> 8) & 0xFF)
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC) & 0xFF)

    # jump to immediate address
    cpu.registers.PC = d16

def RST_n(cpu, n):
    """
    Call subroutine at address n*8.
    For example, RST 1 calls subroutine at address 0x08.
    """
    # Push current PC to stack
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC >> 8) & 0xFF)
    cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
    cpu.write_d8(cpu.registers.SP, (cpu.registers.PC) & 0xFF)

    # Jump to address n*8
    cpu.registers.PC = n * 8