################################################################################
# Misc instructions
################################################################################

def NOP(cpu):
    pass

def STOP(cpu):
    pass

def HALT(cpu):
    pass

def CPL(cpu):
    """Complement (invert) A register"""
    cpu.registers.A = 0xFF - cpu.registers.A
    cpu.registers.n_flag = 1
    cpu.registers.h_flag = 1

def CCF(cpu):
    """flip carry flag"""
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 0 if cpu.registers.c_flag else 1

def SCF(cpu):
    """set carry flag"""
    cpu.registers.n_flag = 0
    cpu.registers.h_flag = 0
    cpu.registers.c_flag = 1
