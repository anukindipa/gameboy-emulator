################################################################################
# Load instructions
################################################################################

# Load 16 bit value pointed by the next two bytes of PC into r16
def LD_r16_d16(cpu, r_name):
    d16 = cpu.read_d16()
    setattr(cpu.registers, r_name, d16)
    
# Copy the value in register r2 into register r1.
def LD_r8_r8(cpu, r1_name, r2_name):
    val = getattr(cpu.registers, r2_name)
    setattr(cpu.registers, r1_name, val)
    
# Load 8 bit value pointed by PC into r8
def LD_r8_d8(cpu, r_name):
    d8 = cpu.read_d8()
    setattr(cpu.registers, r_name, d8)
    
# Copy the byte pointed to by `rname` of type r16 into register r8.
# ex: 0x0a - LD A, [BC]
def LD_r8_m8(cpu, r_name, m8_name):
    address = getattr(cpu.registers, m8_name)
    val = cpu.read_d8(address)
    setattr(cpu.registers, r_name, val)

# Copy the value in register r8 into the byte pointed to by r16 (HL).
# ex: 0x02 - LD [HL], A
def LD_m8_r8(cpu, m8_name, r_name):
    val = getattr(cpu.registers, r_name)
    address = getattr(cpu.registers, m8_name)
    cpu.write_d8(address, val)

# Copy the value d8 into the byte pointed to by HL.
# ex: 0x36 - LD [HL], n8
def LD_m8_d8(cpu, r_name):
    d8= cpu.read_d8()
    address = getattr(cpu.registers, r_name)
    cpu.write_d8(address, d8)


# Copy the byte pointed to by HL into register A, and increment/decrement HL afterwards.
# Increment is sometimes written as ‘LD A,[HL+]’, or ‘LDI A,[HL]’.
# Decrement is sometimes written as ‘LD A,[HL-]’, or ‘LDD A,[HL]’.
# Only used by instruction 0x2A (increment), 0x3A (decrement).
def LD_A_HLID(cpu, increment=True):
    address = cpu.registers.HL
    cpu.registers.A = cpu.read_d8(address)
    if increment:
        cpu.registers.HL = (address + 1) & 0xffff
    else:
        cpu.registers.HL = (address - 1) & 0xffff

# Copy the value in register A into the byte pointed by HL and increment/ decrement HL afterwards.
# Similar to LD_A_HLID but in reverse.
# known as ‘LD [HL+],A’ or ‘LDI [HL],A’ when incrementing, 
# and ‘LD [HL-],A’ or ‘LDD [HL],A’ when decrementing.
# Only used by instruction 0x22 (increment), 0x32 (decrement).
def LD_HLID_A(cpu, increment=True):
    address = cpu.registers.HL
    cpu.write_d8(address, cpu.registers.A)
    if increment:
        cpu.registers.HL = (address + 1) & 0xffff
    else:
        cpu.registers.HL = (address - 1) & 0xffff

# Load to the 8-bit A register, data from the address specified by the 8-bit immediate data n.
# The full 16-bit absolute address is obtained by setting the most significant byte to 0xFF 
# and the least significant byte to the value of n, so the possible range is 0xFF00-0xFFFF.
# Only used by instruction 0xF0.
# confusing opcode reference: https://gekkio.fi/files/gb-docs/gbctr.pdf
def LD_A_d8(cpu):
    address = cpu.read_d8() + 0xff00
    if 0xff00 > address or  address > 0xffff:
        raise ValueError(f"LD_A_d8 address out of range: {address:04x}")
    val = cpu.read_d8(address)
    cpu.registers.A = val

# like LD_A_d8 (0xF0) but in reverse
# Only used by instruction 0xE0.
def LD_d8_A(cpu):
    address = cpu.read_d8() + 0xff00
    if 0xff00 > address or  address > 0xffff:
        raise ValueError(f"LD_A_d8 address out of range: {address:04x}")
    val = cpu.registers.A
    cpu.write_d8(address, val)
    
# Copy the value in register A into the byte at address $FF00+C.
# Only used by instruction 0xE2.
def LDH_C_A(cpu):
    value = cpu.registers.A
    address = 0xff00 + cpu.registers.C
    if 0xff00 > address or  address > 0xffff:
        raise ValueError(f"LHD_d16_A address out of range: {address:04x}")
    cpu.write_d8(address, value)

# Load to the 8-bit A register, data from the address $FF00+C.
# Only used by instruction 0xF2.
def LDH_A_C(cpu):
    address = 0xff00 + cpu.registers.C
    if 0xff00 > address or  address > 0xffff:
        raise ValueError(f"LHD_d16_A address out of range: {address:04x}")
    value = cpu.read_d8(address)
    cpu.registers.A = value


# Copy the value in register A into the byte at address d16
# Where d16 is read from the next two bytes of PC.
# Only used by instruction 0xEA.
def LD_d16_A(cpu):
    val = cpu.registers.A
    address = cpu.read_d16()
    cpu.write_d8(address, val)
    
# Copy the value in byte at address d16 into register A.
# Where d16 is read from the next two bytes of PC.
# Only used by instruction 0xFA.
def LD_A_d16(cpu):
    address = cpu.read_d16()
    value = cpu.read_d8(address)
    cpu.registers.A = value

