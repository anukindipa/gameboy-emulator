class InvalidFlagValue(Exception):
    """Raised when a flag is assigned a value not equal to 0 or 1."""
    pass

class Registers():
    """
    Register emulation
    A,B...L are 8-bit registers
    PC and SP are 16-bit
    AF, BC, DE, HL are 'virtual registers'
    """
    __slots__ = (
    "A", "B", "C", "D", "E", "F", "H", "L",
    "SP", "PC",
    "Z_FLAG", "N_FLAG", "H_FLAG", "C_FLAG",
)

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
        
        # flag helpers
        self.Z_FLAG = 0x80
        self.N_FLAG = 0x40
        self.H_FLAG = 0x20
        self.C_FLAG = 0x10

    # the AF, BC, DE, HL registers are 16 bit registers
    # where the two 8-bit registers A and F are treated as a single register
    # @property allows treating AF like an attribute

    # retrieving values from pair registers
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
    
    # setting register values for pair registers
    @AF.setter
    def AF(self, val):
        """
        takes a 16-bit value `val` 
        and assigns first 8 bits to register A
        and the next 8 bits to register F
        """
        self.A = (val & 0xFF00) >> 8
        self.F = val & 0xFF
    @BC.setter
    def BC(self, val):
        self.B = (val & 0xFF00) >> 8
        self.C = val & 0xFF
    @DE.setter
    def DE(self, val):
        self.D = (val & 0xFF00) >> 8
        self.E = val & 0xFF
    @HL.setter
    def HL(self, val):
        self.H = (val & 0xFF00) >> 8
        self.L = val & 0xFF
        
    # flag handling

    # helper function for reading flag values
    def _get_flag(self, flag):
        return bool(self.F & flag)
    
    # helper function for getting flag values
    def _set_flag(self, flag, value):
        if value not in [1,0]:
            raise InvalidFlagValue(f"flag values must be 0 or 1. but {value} recieved")
        if value:
            self.F = self.F | flag
        else:
            # (0xFF - flag) is the easiest way to get the bitwise not
            # operation for our 16bit ints
            self.F = self.F & (0xFF - flag)
    
    # getting flag values
    @property
    def z_flag(self):
        return self._get_flag(self.Z_FLAG)
    @property
    def n_flag(self):
        return self._get_flag(self.N_FLAG)
    @property
    def h_flag(self):
        return self._get_flag(self.H_FLAG)
    @property
    def c_flag(self):
        return self._get_flag(self.C_FLAG)
            
    # setting flag values
    @z_flag.setter
    def z_flag(self, value):
        self._set_flag(self.Z_FLAG, value)
    @n_flag.setter
    def n_flag(self, value):
        self._set_flag(self.N_FLAG, value)
    @h_flag.setter
    def h_flag(self, value):
        self._set_flag(self.H_FLAG, value)
    @c_flag.setter
    def c_flag(self, value):
        self._set_flag(self.C_FLAG, value)
