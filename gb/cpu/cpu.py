from registers import Registers

class CPU():
    def __init__(self):
        self.reg = Registers()
        
    def fetch(self):
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def step(self):
        # read do fetch()
        self.reg.PC += 1
        pass