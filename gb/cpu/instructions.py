"""
r8 is a normal register like A, B
r16 is a 'pair' register like DE, HL

d16 is a 16 bit value
"""

def NOP():
    pass

def LD_r16_d16(registers, r_name, d16):
    setattr(registers, r_name, d16)
    
def INC_r16(registers, r_name):
    val = getattr(registers, r_name)
    # wrap around
    val = (val+1) & 0xff 
    setattr(registers, r_name, val)
    
    registers.z_flag = int(val==0)
    registers.n_flag = 0
    # finish c_flag


