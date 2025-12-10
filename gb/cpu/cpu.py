################################################################################
# CPU module
# Handles the fetch-decode-execute cycle of the CPU
################################################################################

from registers import Registers
from instructions import OP_Handler
# TODO: decide if I want to import MMU here or pass it from outside
# from gb.mmu import MMU

class CPU():
    def __init__(self, mmu):
        self.reg = Registers()
        self.memory = mmu
        
    def fetch(self):
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def step(self):
        # read do fetch()
        #     read opcode pointed by PC
        self.reg.PC += 1

        # if opcode == 0xCB:
        #     handle the second table

        # else:
        #     handle opcode
        pass
    
    def read_d8(self, address=None):
        if address is None:
            address = self.reg.PC
            # TOD: check if this is correct
            self.reg.PC += 1

    def read_d16(self, address=None):
        pass