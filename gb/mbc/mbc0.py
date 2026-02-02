# No MBC 
# for simple roms without bank switching like tetris

class MBC0():
    def __init__(self, rom_path):
        self._rom_data = bytearray(0x8000)
        if not rom_path:
            # for testing with no rom
            return

        with open(rom_path, "rb") as f:
            rom_bytes = f.read()
            rom_size = min(len(rom_bytes), 0x8000)
            self._rom_data = bytearray(rom_bytes[:rom_size])
    
    def read_byte(self, address):
        if address < 0x8000:
            return self._rom_data[address]
        else:
            raise ValueError("MBC0 ERROR: cpu tried reading from 0x{:04X}".format(address))
    
    def write_byte(self, address, value):
        # MBC0 does not support writing to ROM
        pass 