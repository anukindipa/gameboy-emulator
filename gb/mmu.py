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
# FF00–FF7F  -> IO registers (joypad etc.)
# FF80–FFFE  -> High RAM (HRAM)
# FFFF       -> Interrupt Enable register

from gb.util.ppu_modes import PPU_MODES

class MMU():
    def __init__(self, mbc):
        # Cartridge MBC (Memory Bank Controller)
        # Handles bytes from 0x0000 to 0x7FFF and 0xA000 to 0xBFFF
        # (ROM and External RAM)
        self.mbc = mbc
        
        self.boot_rom = bytearray(0x100)
        
        # Vram: 8KB
        self.vram = bytearray(0x2000)
        
        # External RAM: 8KB - managed by MBC
        
        # Work RAM: 8KB
        self.wram = bytearray(0x2000)
        
        # I'll not implement Echo RAM for now, as its useless

        # OAM: 160 bytes
        self.oam = bytearray(0xA0)
        
        # Not Usable: 96 bytes

        # IO Registers: 128 bytes
        self.io_regs = bytearray(0x80)

        # High RAM: 127 bytes
        self.hram = bytearray(0x7F)

        # Interrupt Enable register
        self.ie_reg = 0x00

        # PPU mode handled by MMU
        # see gb/ppu/__init__.py and https://gbdev.io/pandocs/Rendering.html
        self.ppu_mode = PPU_MODES.OAM_SCAN  
        
        # boot Rom setup
        try:
            # read 256 bytes from the boot rom
            # rom taken from https://gbdev.gg8.se/files/roms/bootroms/
            with open("gb/boot/dmg_boot.gb", "rb") as f:
                self.boot_rom = f.read(256)
            self.boot_rom_enabled = True

        except FileNotFoundError:
            self.boot_rom_enabled = False
            """
            TODO: add these to cpu init
            self.registers.SP = 0xFFFE  # set stack pointer to default value if no boot rom
            self.registers.PC = 0x0100  # set program counter to default value if no boot rom
            self.registers.AF = 0x01B0  # Game boy register state after boot
            self.registers.BC = 0x0013
            self.registers.DE = 0x00D8
            self.registers.HL = 0x014D
            """
            

        
    def read_byte(self, address, ppu_read = False):
        # read from boot rom if enabled
        if self.boot_rom_enabled and address < 0x100:
            return self.boot_rom[address]

        # done with boot rom or boot rom accessed beyond 0x00FF
        if address < 0x8000:
            # ROM bank 0 and switchable bank
            return self.mbc.read_byte(address)

        # VRAM
        if 0x8000 <= address < 0xA000:
            if self.ppu_mode == PPU_MODES.PIXEL_TRANSFER and not ppu_read:
                # cpu cant read vram during pixel transfer
                #  -  https://gbdev.io/pandocs/Rendering.html
                return 0xFF
            return self.vram[address - 0x8000]

        if 0xA000 <= address < 0xC000:
            # External RAM managed by MBC
            # pokemon sav files are stored here
            return self.mbc.read_byte(address)

        if 0xC000 <= address < 0xE000:
            # working ram
            return self.wram[address - 0xC000]

        if 0xE000 <= address < 0xFE00:
            # Echo RAM (not usable, mirrors WRAM)
            return self.wram[address - 0xE000]

        if 0xFE00 <= address < 0xFEA0:
            # OAM
            if self.ppu_mode in (PPU_MODES.OAM_SCAN, PPU_MODES.PIXEL_TRANSFER) and not ppu_read:
                # cpu cant read oam during oam scan and pixel transfer
                #  -  https://gbdev.io/pandocs/Rendering.html
                return 0xFF
            return self.oam[address - 0xFE00]

        if 0xFEA0 <= address < 0xFF00:
            # Not Usable
            return 0xFF
        
        if 0xFF00 <= address < 0xFF80:
            # IO Registers
            idx = address - 0xFF00
            # Joypad register (FF00) handling
            if address == 0xFF00:
                # No keys pressed: lower nibble all high (bits 0-3 = 1)
                # Upper bits: 1 1 and selection bits (P14/P15)
                return 0xC0 | self.joyp_select | 0x0F
            return self.io_regs[idx]
        
        if 0xFF80 <= address < 0xFFFF:
            # High RAM
            return self.hram[address - 0xFF80]

        # Interrupt Enable register
        # technically is not readable, but needed for functionality
        raise NotImplementedError("Interrupt Enable register is not readable yet.")
        return self.ie_reg


    def write_byte(self, address, value, ppu_write = False):
        # TODO: handle writes to boot rom area for disabling boot rom
        # TODO: handle MBC writes
        
        # VRAM
        if 0x8000 <= address < 0xA000:
            if self.ppu_mode == PPU_MODES.PIXEL_TRANSFER and not ppu_write:
                # cpu cant write to vram during pixel transfer
                #  -  https://gbdev.io/pandocs/Rendering.html
                return 
            self.vram[address - 0x8000] = value
            return

        if 0xA000 <= address < 0xC000:
            # External RAM managed by MBC
            # pokemon sav files are stored here
            self.mbc.write_byte(address, value)
            return

        if 0xC000 <= address < 0xE000:
            # working ram
            self.wram[address - 0xC000] = value
            return

        if 0xE000 <= address < 0xFE00:
            # Echo RAM (not usable)
            print("Warning: Writing to Echo RAM (0xE000-0xFDFF) is not recommended.")
            self.wram[address - 0xE000] = value
            return

        if 0xFE00 <= address < 0xFEA0:
            # OAM
            if self.ppu_mode in (PPU_MODES.OAM_SCAN, PPU_MODES.PIXEL_TRANSFER) and not ppu_write:
                # cpu cant write to oam during oam scan and pixel transfer
                #  -  https://gbdev.io/pandocs/Rendering.html
                return 

            self.oam[address - 0xFE00] = value
            return

        if 0xFEA0 <= address < 0xFF00:
            # Not Usable
            print("Warning: Writing to Not Usable area (0xFEA0-0xFEFF) has no effect.")
            return
        
        if address == 0xFF50:
            # disable boot ROM; subsequent reads go to cartridge
            print("Boot ROM disabled.")
            self.boot_rom_enabled = False
            return

        if 0xFF00 <= address < 0xFF80:
            # IO Registers
            idx = address - 0xFF00
            if address == 0xFF00:
                # Store selection bits (bits 4-5). Others ignored for now.
                self.joyp_select = value & 0x30
                return
            if address == 0xFF40:
                # LCDC register - important for display
                print(f"LCDC written: {value:#04x}")
            self.io_regs[idx] = value
            return 
        
        if 0xFF80 <= address < 0xFFFF:
            # High RAM
            self.hram[address - 0xFF80] = value
            return

        # Interrupt Enable register
        if address == 0xFFFF:
            ValueError("Interrupt Enable register is not writable yet.")


# for testing functionality
if __name__ == "__main__":
    def read_boot_rom():
        # print content of boot rom
        mmu = MMU()
        for byte in mmu.boot_rom:
           print(f"{byte:02x}", end=" ")
    
    read_boot_rom()