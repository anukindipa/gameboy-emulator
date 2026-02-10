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
from gb.timers import Timer

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

        # IO Registers: 128 bytes (0xFF00 - 0xFF7F)
        self.io_regs = bytearray(0x80)

        # High RAM: 127 bytes
        self.hram = bytearray(0x7F)

        # Interrupt Enable register (0xFFFF)
        self.ie_reg = 0x00

        # Interrupt Flag register (0xFF0F)
        # technically in IO registers, but easier to handle separately
        self.if_reg = 0x00

        # PPU mode handled by MMU
        # see gb/ppu/__init__.py and https://gbdev.io/pandocs/Rendering.html
        self.ppu_mode = PPU_MODES.OAM_SCAN 
        
        # Joypad select bits
        self.joyp_select = 0x00
        
        # Button states: (direction_buttons, action_buttons)
        # Each nibble: bit 0=Right/A, 1=Left/B, 2=Up/Select, 3=Down/Start
        # 0 = pressed, 1 = not pressed
        self.button_states = (0x0F, 0x0F)  # All buttons not pressed initially
        
        # Initialize palette registers with default values
        # BGP (0xFF47): Background palette - default 0xFC (11 11 11 00)
        # Maps: 0->white, 1->light gray, 2->dark gray, 3->black
        self.io_regs[0x47] = 0xFC
        
        # OBP0 (0xFF48): Object palette 0 - default 0xFF (11 11 11 11)
        self.io_regs[0x48] = 0xFF
        
        # OBP1 (0xFF49): Object palette 1 - default 0xFF (11 11 11 11)
        self.io_regs[0x49] = 0xFF
        
        # LCDC (0xFF40): LCD Control - default 0x91 (screen on, BG on)
        self.io_regs[0x40] = 0x91

        # For DMA Transfer
        self.dma_transfer_enabled = False
        self.dma_transfer_index = 0
        
        # Timers
        self.timer = Timer()
        
        # boot Rom setup
        try:
            # read 256 bytes from the boot rom
            # rom taken from https://gbdev.gg8.se/files/roms/bootroms/
            with open("gb/boot/dmg_boot.gb", "rb") as f:
                self.boot_rom = f.read(256)
            self._boot_rom_enabled = True

        except FileNotFoundError:
            self._boot_rom_enabled = False
     
    @property
    def boot_rom_enabled(self):
        """Whether the boot ROM is currently mapped (FF50 == 0)."""
        return self._boot_rom_enabled
  
    @boot_rom_enabled.setter
    def boot_rom_enabled(self, value):
        self._boot_rom_enabled = bool(value)
            
    def read_byte(self, address, ppu_read = False, transfer_read = False):
        # During DMA Transfer only HRAM can be read (PPU can still read for rendering)
        if (self.dma_transfer_enabled and address < 0xFF80 and not transfer_read and not ppu_read):
            return 0xFF

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

        # IO Registers
        # 0xFF00 - 0xFF7F

        # Joypad register (FF00) handling
        if address == 0xFF00:
            # Build joypad register value
            # Bits 7-6: Always 1
            # Bits 5-4: Selection bits (from joyp_select)
            # Bits 3-0: Button states based on selection
            joypad_value = 0xC0 | self.joyp_select
            
            # Determine which button set to return based on selection
            # Selection bits are inverted (0 = selected, 1 = not selected)
            direction_buttons, action_buttons = self.button_states
            
            if (self.joyp_select & 0x10) == 0:
                # P14 selected (bit 4 = 0): Return direction buttons
                joypad_value |= direction_buttons
                # print(f"[MMU] Read 0xFF00: P14 selected, returning direction: {joypad_value:02X}")
            elif (self.joyp_select & 0x20) == 0:
                # P15 selected (bit 5 = 0): Return action buttons
                joypad_value |= action_buttons
                # print(f"[MMU] Read 0xFF00: P15 selected, returning action: {joypad_value:02X}")
            else:
                # Nothing selected: all button bits high
                joypad_value |= 0x0F
                # print(f"[MMU] Read 0xFF00: Nothing selected, returning: {joypad_value:02X}")
            
            return joypad_value

        # DIV timer register
        if address == 0xFF04:
            return self.timer.DIV
        
        if address == 0xFF05:
            print(f"Read TIMA: {self.timer.TIMA:#04x}")
            return self.timer.TIMA

        # Interrupt Flag register
        if address == 0xFF0F:
            return self.if_reg

        if address == 0xFF50:
            # Boot ROM disable register: 0 = enabled, 1 = disabled
            return 0x00 if self._boot_rom_enabled else 0x01
        
        # rest of IO registers
        if 0xFF00 <= address < 0xFF80:
            # IO Registers
            idx = address - 0xFF00
            return self.io_regs[idx]
        
        if 0xFF80 <= address < 0xFFFF:
            # High RAM
            return self.hram[address - 0xFF80]

        # Interrupt Enable register (0xFFFF)
        return self.ie_reg


    def write_byte(self, address, value, ppu_write = True, transfer_write = False):
        # TODO: handle writes to boot rom area for disabling boot rom
        # TODO: handle MBC writes
        # TODO: fix timing issue and make it work when ppu_write is False (currently just for testing)

        # During DMA Transfer only HRAM can be written to (PPU can still write for rendering)
        if (self.dma_transfer_enabled and address < 0xFF80 and not transfer_write and not ppu_write):
            return
        
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
            print(f"Warning: Writing to Not Usable area (0xFEA0-0xFEFF) has no effect. {address:#04x} <- {value:#04x}")
            return
        
        # IO Registers
        
        # DIV timer register: writing any value resets it to 0
        if address == 0xFF04:
            self.timer.DIV = 0x00
            self.timer.div_counter = 0
            return
        
        # Interrupt Flag register
        if address == 0xFF0F:
            if value != self.if_reg:  # Only print on change
                # print(f"[MMU] Writing to IF register: {value:#04x} (was {self.if_reg:#04x}) - Bits set: ", end="")
                interrupt_names = ["V-Blank", "LCD STAT", "Timer", "Serial", "Joypad"]
                bits_set = [interrupt_names[i] for i in range(5) if value & (1 << i)]
                # print(", ".join(bits_set) if bits_set else "None")
            self.if_reg = value
            return
        
        # LY changes can also trigger STAT interrupts
        if address == 0xFF44:
            if not ppu_write:
                return
            self.io_regs[0x44] = value
            # Update LYC=LY flag and check for LCD STAT interrupt
            self._update_lyc_flag()
            return

        # LYC changes can trigger STAT interrupts, so handle writes to LYC (0xFF45) here
        if address == 0xFF45:
            self.io_regs[0x45] = value
            # Update LYC=LY flag and check for LCD STAT interrupt
            self._update_lyc_flag()
            return

        # Enable DMA Transfer from value << 8
        if address == 0xFF46:
            self.dma_transfer_enabled = True
            self.dma_transfer_source = value << 8
            self.dma_transfer_index = 0
        

        # Rest of IO Registers
        if 0xFF00 <= address < 0xFF80:
            idx = address - 0xFF00
            if address == 0xFF00:
                # Store selection bits (bits 4-5). Others ignored for now.
                self.joyp_select = value & 0x30
                return
            if address == 0xFF50:
                # Writing non-zero disables boot ROM; zero keeps it enabled
                self._boot_rom_enabled = (value & 0x01) == 0
                return
            if address == 0xFF40:
                # LCDC register - important for display
                print(f"LCDC written: {value:#04x}")
            if address == 0xFF47:
                # BGP - Background palette
                print(f"BGP (background palette) set to: {value:#04x}")
            if address == 0xFF48:
                # OBP0 - Object palette 0
                print(f"OBP0 (sprite palette 0) set to: {value:#04x}")
            if address == 0xFF49:
                # OBP1 - Object palette 1
                print(f"OBP1 (sprite palette 1) set to: {value:#04x}")
            self.io_regs[idx] = value
            return 
        
        if 0xFF80 <= address < 0xFFFF:
            # High RAM
            self.hram[address - 0xFF80] = value
            return
        
        # Interrupt Enable register (0xFFFF)
        if address == 0xFFFF:
            self.ie_reg = value
            return

    def _update_lyc_flag(self):
        """Update STAT bit 2 (LYC=LY flag) and possibly trigger LCD STAT interrupt"""
        lyc = self.read_byte(0xFF45, ppu_read=True)  # LYC register
        ly = self.read_byte(0xFF44, ppu_read=True)   # LY register
        stat = self.read_byte(0xFF41, ppu_read=True)
        
        if ly == lyc:
            # Set LYC=LY flag (bit 2)
            stat |= 0x04
            
            # If LYC=LY interrupt enabled (bit 6), trigger LCD STAT interrupt
            if stat & 0x40:
                self.if_reg |= 0x02  # LCD STAT interrupt is bit 1
        else:
            # Clear LYC=LY flag
            stat &= ~0x04
        
        self.write_byte(0xFF41, stat, ppu_write=True)


# for testing functionality
if __name__ == "__main__":
    def read_boot_rom():
        # print content of boot rom
        mmu = MMU()
        for byte in mmu.boot_rom:
           print(f"{byte:02x}", end=" ")
    
    read_boot_rom()
