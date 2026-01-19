################################################################################
# CPU module
# Handles the fetch-decode-execute cycle of the CPU
################################################################################

from .registers import Registers
from .instructions import OP_Handler
from gb.util.bit_ops import d8_to_s8
# TODO: decide if I want to import MMU here or pass it from outside
# from gb.mmu import MMU

class CPU():
    def __init__(self, mmu):
        # cpu registers
        self.registers = Registers()

        # memory management unit
        self.memory = mmu

        # opcode handler
        self.op_handler = OP_Handler()


    def step(self):
        # for logging
        PC_before = self.registers.PC

        # fetch
        # PC += 1 is handled by read_d8
        opcode = self.read_d8()
        
        # decode and execute
        cycles = self.op_handler.execute_opcode(self, opcode)

        # Optional debug logging; comment out for performance
        # print(f"Opcode {hex(opcode)} took {cycles:-2} cycles. PC: {hex(PC_before)}")

        return cycles

    
    def read_d8(self, address=None):
        if address is None:
            address = self.registers.PC
            # TODO: check if this is correct
            self.registers.PC += 1
        mem = self.memory.read_byte(address)
        if mem < 0 or mem > 0xFF:
            raise ValueError(f"read_d8 value must be between 0 and 255, got {mem}")
        return mem
    
    def read_s8(self, address=None):
        value = self.read_d8(address)
        return d8_to_s8(value)

    def read_d16(self, address=None):
        # TODO: check if read_d16 is every called with addread not None
        if address:
            raise ValueError("read_d16 with address not None not implemented yet")

        lsb = self.read_d8()
        msb = self.read_d8()
        v = (msb << 8) | lsb
        if v < 0 or v > 0xFFFF:
            raise ValueError(f"read_d16 value out of range, v = {v}, address = {hex(address)}, lsb = {lsb}, msb = {msb}")
        return v



    def write_d8(self, address=None, value=0):
        if address is None:
            address = self.registers.PC
        if value < 0 or value > 0xFF:
            raise ValueError(f"write_d8 value must be between 0 and 255, got {value} at address {hex(address)}")
        self.memory.write_byte(address, value) 
