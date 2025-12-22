class PPU():
    def __init__(self, mmu):
        # access to memory (vram, oam, etc.), shared with cpu
        self.mmu = mmu

        # initial mode is HBlank
        self.mode = 0

        self.line_cycles = 0  # cycles spent on current line

    def step(self, cycles):
        pass

    def render_scanline(self):
        pass 
        
        
    ###########################################################################
    # PPU mode 
    ###########################################################################
    # While the PPU is accessing some video-related memory, that memory is
    # inaccessible to the CPU (writes are ignored, and reads return garbage values).
    #  -  https://gbdev.io/pandocs/Rendering.html
    # So ppu_mode will be handled by by the mmu
    @property
    def mode(self):
        return self.mmu.ppu_mode
    @mode.setter
    def mode(self, value):
        self.mmu.ppu_mode = value
    ###########################################################################
        

    ###########################################################################
    # LY register (0xFF44)
    ###########################################################################
    @property
    def ly(self):
        return self.mmu.read_byte(0xff44)
    @ly.setter
    def ly(self, value):
        self.mmu.write_byte(0xff44, value) 
    ###########################################################################

