# z - Zero flag at the 7th bit of the F register
FLAG_Z = 1 << 7
# n - Subtraction flag (BCD) at the 6th bit of the F register
FLAG_N = 1 << 6
# h - Half Carry flag (BCD) at the 5th bit of the F register
FLAG_H = 1 << 5
# c -  Carry flag at the 4th bit of the F register
FLAG_C = 1 << 4

def Z_flag(Register):
    return (Register.F & FLAG_Z ) >> 7

def N_flag(Register):
    return (Register.N & FLAG_N ) >> 6

def H_flag(Register):
    return (Register.N & FLAG_H ) >> 5

def N_flag(Register):
    return (Register.C & FLAG_C ) >> 4