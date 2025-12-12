################################################################################
# CPU module
# Handles the fetch-decode-execute cycle of the CPU
################################################################################

from .registers import Registers
from .instructions import OP_Handler
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
        # fetch
        # PC += 1 is handled by read_d8
        opcode = self.read_d8()

        # decode and execute
        cycles = self.OP_Handler.execute_opcode(self, opcode)
        
        # TODO: handle cycles, interrupts, ppu steps, etc.

    
    def read_d8(self, address=None):
        if address is None:
            address = self.registers.PC
            # TODO: check if this is correct
            self.registers.PC += 1

        return self.memory.read_byte(address)

    def read_d16(self, address=None):
        pass

    def write_d8(self, address=None):
        pass
