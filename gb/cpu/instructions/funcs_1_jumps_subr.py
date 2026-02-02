"""Jumps and subroutine instructions"""

def JR_cc_s8(cpu, condition):
    """Jump relative by signed immediate d16 if condition is True"""
    # PC is incremented regardless of condition
    offset = cpu.read_s8()

    if not condition:
        return

    # adding is correct as PC is incremented once reading opcode 
    # and again after reading d8:
    # https://www.reddit.com/r/EmuDev/comments/jmo5x1/gameboy_0x20_instruction/
    cpu.registers.PC = (cpu.registers.PC + offset) & 0xFFFF

def RET(cpu):
    # Restore PC from stack
    lsb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    msb = cpu.read_d8(cpu.registers.SP)
    cpu.registers.SP = (cpu.registers.SP + 1) & 0xFFFF
    
    # Set PC to the address popped from stack
    cpu.registers.PC = (msb << 8) | lsb