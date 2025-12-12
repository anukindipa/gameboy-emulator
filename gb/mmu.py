################################################################################
# Memory Management Unit class
################################################################################

# Memory Map (https://gbdev.io/pandocs/Memory_Map.html):
# 0000–3FFF  -> ROM bank 0 (game code, fixed)
# 4000–7FFF  -> Switchable ROM bank (From cartridge, switchable bank via mapper (if any))
# 8000–9FFF  -> VRAM (graphics tiles)
# A000–BFFF  -> External RAM (save RAM, MBC-controlled)
# C000–DFFF  -> WRAM (working RAM)
# E000–FDFF  -> Echo RAM (mirror of WRAM, Nintendo says "do not use")
# FE00–FE9F  -> OAM (Object Attribite Memory - sprite table)
# FEA0–FEFF  -> Not Usable
# FF00–FF7F  -> IO registers (joypad)
# FF80–FFFE  -> High RAM (HRAM)
# FFFF       -> Interrupt Enable register


class MMU():
    def __init__(self, mbc):
        # Cartridge MBC (Memory Bank Controller)
        # Handles bytes from 0x0000 to 0x7FFF and 0xA000 to 0xBFFF
        # (ROM and External RAM)
        self.mbc = mbc

        # TODO: decide who gets VRAM mmu or mbc
        # Vram: 8KB
        self.vram = bytearray(0x2000)
        
        # Work RAM: 8KB
        self.wram = bytearray(0x2000)
        
        # I'll not implement Echo RAM for now, as its useless

        # OAM: 160 bytes
        self.oam = bytearray(0xA0)

        # IO Registers: 128 bytes
        self.io_regs = bytearray(0x80)

        # High RAM: 127 bytes
        self.hram = bytearray(0x7F)

        # interrupt enable register
        self.interrupt_enable = 0x00
        
        # boot Rom setup
        try:
            # read 256 bytes from the boot rom
            # rom taken from https://gbdev.gg8.se/files/roms/bootroms/
            with open("gb/boot/dmg_boot.gb", "rb") as f:
                self.boot_rom = f.read(256)
            self.boot_rom_enabled = True

        except FileNotFoundError:
            self.boot_rom_enabled = False
            # TODO: implement boot rom missing case

        
    def read_byte(self, address):
        # read from boot rom if enabled
        if self.boot_rom_enabled and address < 0x100:
            return self.boot_rom[address]


    def write_byte(self, address, value):
        pass

# for testing functionality
if __name__ == "__main__":
    def read_boot_rom():
        # print content of boot rom
        mmu = MMU()
        for byte in mmu.boot_rom:
           print(f"{byte:02x}", end=" ")
    
    read_boot_rom()