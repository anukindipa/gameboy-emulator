class Registers():
    """
    Register emulation
    A,B...L are 8-bit registers
    PC and SP are 16-bit
    AF, BC, DE, HL are 'virtual registers'
    """
    # setup the registers
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.H = 0
        self.L = 0
        
        # stack pointer
        self.SP = 0
        # program counter
        self.PC = 0

    # the AF, BC, DE, HL registers are 16 bit registers
    # where the two 8-bit registers A and F are treated as a single register
    # @property allows treating AF like an attribute

    @property
    def AF(self):
        return (self.A << 8) | self.F
     
    @property
    def BC(self):
        return (self.B << 8) | self.C

    @property
    def DE(self):
        return (self.D << 8) | self.E

    @property
    def HL(self):
        return (self.H << 8) | self.L
    
    def set_AF(self, val):
        """
        takes a 16-bit value `val` 
        and assigns first 8 bits to register A
        and the next 8 bits to register F
        """
        self.A = (val & 0xFF00) >> 8
        self.F = val & 0xFF

    def set_BC(self, val):
        self.B = (val & 0xFF00) >> 8
        self.C = val & 0xFF
    def set_DE(self, val):
        self.D = (val & 0xFF00) >> 8
        self.E = val & 0xFF
    def set_HL(self, val):
        self.H = (val & 0xFF00) >> 8
        self.L = val & 0xFF
        