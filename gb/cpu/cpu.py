from registers import Registers
from gb.mmu import MMU

class CPU():
    def __init__(self):
        self.reg = Registers()
        self.memory = MMU()
        
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
    
    def read_d8():
        pass

    def read_d16():
        pass