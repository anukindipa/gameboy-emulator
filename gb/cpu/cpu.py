################################################################################
# CPU module
# Handles the fetch-decode-execute cycle of the CPU
################################################################################

from gb import cpu
from .registers import Registers
from .instructions import OP_Handler
from gb.util.bit_ops import d8_to_s8
from gb.interupts import interrupt_handler

class CPU():
    def __init__(self, mmu):
        # cpu registers
        self.registers = Registers()

        # memory management unit
        self.mmu = mmu

        # opcode handler
        self.op_handler = OP_Handler()
        
        # Interupt Master Enable flag
        self.ime = False
        
        # When EI is called, the IME is enabled after the next instruction
        self.ime_requested = 0
        
        # Halted state
        self.halted = False
        
        # if not self.mmu.boot_rom_enabled:
        #     # Setup CPU state as if boot rom has been run
        #     self.no_boot_rom_setup()  

    def step(self):
        # Handle interrupts before executing next instruction
        interrupt_cycles = interrupt_handler(self)
        if interrupt_cycles > 0:
            return interrupt_cycles
        
        # Halted state consumes 4 cycles
        if self.halted:
            return 4  

        # for logging
        PC_before = self.registers.PC

        # fetch
        # PC += 1 is handled by read_d8
        opcode = self.read_d8()
        
        # decode and execute
        cycles = self.op_handler.execute_opcode(self, opcode)

        # Handle DMA Transfer
        for _ in range(cycles//4):  # DMA transfer happens every 4 cycles
            if self.mmu.dma_transfer_enabled:
                read_idx = self.mmu.dma_transfer_source + self.mmu.dma_transfer_index
                data = self.mmu.read_byte(read_idx, ppu_read = True, transfer_read = True)
                self.mmu.write_byte(0xFE00 + self.mmu.dma_transfer_index, data, ppu_write = True, transfer_write = True)
                self.mmu.dma_transfer_index = self.mmu.dma_transfer_index + 1

                # end dma transfer after 160 bytes
                if self.mmu.dma_transfer_index == 160:
                    self.mmu.dma_transfer_enabled = False

        # Optional debug logging; comment out for performance
        # print(f"Opcode {hex(opcode)} took {cycles:-2} cycles. PC: {hex(PC_before)}")
        
        # Handle IME request from EI instruction
        if self.ime_requested > 0:
            self.ime_requested -= 1
            if self.ime_requested == 0:
                self.ime = True

        return cycles

    
    def read_d8(self, address=None):
        if address is None:
            address = self.registers.PC
            # TODO: check if this is correct
            self.registers.PC += 1
        mem = self.mmu.read_byte(address)
        if mem < 0 or mem > 0xFF:
            raise ValueError(f"read_d8 value must be between 0 and 255, got {mem}")
        return mem
    
    def read_s8(self, address=None):
        value = self.read_d8(address)
        return d8_to_s8(value)

    def read_d16(self, address=None):
        # TODO: check if read_d16 is every called with addread not None
        if address:
            raise ValueError("read_d16 with address not None not implemented yet")

        lsb = self.read_d8()
        msb = self.read_d8()
        v = (msb << 8) | lsb
        if v < 0 or v > 0xFFFF:
            raise ValueError(f"read_d16 value out of range, v = {v}, address = {hex(address)}, lsb = {lsb}, msb = {msb}")
        return v



    def write_d8(self, address=None, value=0):
        if address is None:
            address = self.registers.PC
        if value < 0 or value > 0xFF:
            raise ValueError(f"write_d8 value must be between 0 and 255, got {value} at address {hex(address)}")
        self.mmu.write_byte(address, value) 

    def no_boot_rom_setup(self):
        """Setup CPU and MMU state as if boot rom has been run"""
        self.registers.AF = 0x01B0
        self.registers.BC = 0x0013
        self.registers.DE = 0x00D8
        self.registers.HL = 0x014D
        self.registers.SP = 0xFFFE
        self.registers.PC = 0x0100

        # MMU state setup
        self.mmu.io_regs[0x40] = 0x91  # LCDC
        self.mmu.io_regs[0x47] = 0xFC  # BGP
        self.mmu.io_regs[0x48] = 0xFF  # OBP0
        self.mmu.io_regs[0x49] = 0xFF  # OBP1;
