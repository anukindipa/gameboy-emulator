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
        # sometimes A and F are read from memory so are treated as uint8.
        # But that causes an error when combining FA to make a 16bit value.
        # so we ensure A and F are treated as int here.
        af = (int(self.A) << 8) | int(self.F)
        if af < 0 or af > 0xFFFF:
            raise ValueError(f"AF register value out of range: {af}")
        return af

    @property
    def BC(self):
        bc = (int(self.B) << 8) | int(self.C)
        if bc < 0 or bc > 0xFFFF:
            raise ValueError(f"BC register value out of range: {bc}")
        return bc

    @property
    def DE(self):
        de = (int(self.D) << 8) | int(self.E)
        if de < 0 or de > 0xFFFF:
            raise ValueError(f"DE register value out of range: {de}")
        return de

    @property
    def HL(self):
        hl = (int(self.H) << 8) | int(self.L)
        if hl < 0 or hl > 0xFFFF:
            raise ValueError(f"HL register value out of range: {hl}")
        return hl
    
    # setting register values for pair registers
    @AF.setter
    def AF(self, val):
        """
        takes a 16-bit value `val` 
        and assigns first 8 bits to register A
        and the next 8 bits to register F
        """
        if val < 0 or val > 0xFFFF:
            raise ValueError(f"AF register value out of range: {val}")
        self.A = (val & 0xFF00) >> 8
        self.F = val & 0xF0
        # updating F register also updates flag values
        # TODO: check if this is correct
        self.z_flag =  bool(self.F & self.Z_FLAG)
        self.n_flag =  bool(self.F & self.N_FLAG)
        self.h_flag =  bool(self.F & self.H_FLAG)
        self.c_flag =  bool(self.F & self.C_FLAG)


    @BC.setter
    def BC(self, val):
        if val < 0 or val > 0xFFFF:
            raise ValueError(f"BC register value out of range: {val}")
        self.B = (val & 0xFF00) >> 8
        self.C = val & 0xFF
    @DE.setter
    def DE(self, val):
        if val < 0 or val > 0xFFFF:
            raise ValueError(f"DE register value out of range: {val}")
        self.D = (val & 0xFF00) >> 8
        self.E = val & 0xFF
    @HL.setter
    def HL(self, val):
        if val < 0 or val > 0xFFFF:
            raise ValueError(f"HL register value out of range: {val}")
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

    def print_registers(self):
        """Debug function to print all register values"""
        print(f"A: {hex(self.A)} F: {hex(self.F)}", end =' ')
        print(f"B: {hex(self.B)} C: {hex(self.C)}", end =' ')
        print(f"D: {hex(self.D)} E: {hex(self.E)}", end =' ')
        print(f"H: {hex(self.H)} L: {hex(self.L)}", end =' ')
        print(f"SP: {hex(self.SP)} PC: {hex(self.PC)}", end=' ')
        print(f"Flags - Z: {self.z_flag} N: {self.n_flag} H: {self.h_flag} C: {self.c_flag}")