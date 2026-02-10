#TODO: Handle timer stops after HALT and STOP instructions

class Timer():
    def __init__(self):
        self.DIV = 0x00  # Divider Register (0xFF04)
        self.TIMA = 0x00 # Timer Counter (0xFF05)
        self.TMA = 0x00  # Timer Modulo (0xFF06)
        self.TAC = 0x00  # Timer Control (0xFF07)

        self.div_counter = 0
        self.tima_counter = 0
    
    def step(self, cycles):
        # Increment DIV every 256 cycles
        self.div_counter += cycles
        if self.div_counter >= 256:
            self.div_counter -= 256
            self.DIV = (self.DIV + 1) & 0xFF
