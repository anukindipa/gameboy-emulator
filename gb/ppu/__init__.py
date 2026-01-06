from gb.util import PPU_MODES

class PPU():
    def __init__(self, mmu):
        # access to memory (vram, oam, etc.), shared with cpu
        self.mmu = mmu

        # initial mode is HBlank
        self.mode = PPU_MODES.H_BLANK

        # cycle limit for current mode
        self.cycle_limit =PPU_MODES.H_BLANK.value

        # cycles spent in current mode
        self.cycles_spent = 0  
        
        # ly - current scanline (0-153) also stored in LY register (0xFF44)
        # will be handled by @ly.setter bellow
        self.ly = 0

        # lx - x-coordinate of the pixel being rendered 
        self.lx = 0

    ###########################################################################
    # PPU mode 
    ###########################################################################
    # While the PPU is accessing some video-related memory, that memory is
    # inaccessible to the CPU (writes are ignored, and reads return garbage values).
    #  -  https://gbdev.io/pandocs/Rendering.html
    # ppu_mode will be handled by the mmu and cpu will access vram when allowed
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
    
    def set_state(self, state):
        """
        used when changing ppu mode
        1. update cycles spent by subtracting cycle limit and
              carry over extra cycles
        2. change mode
        3. set new cycle limit
        """
        # carry over extra cycles
        # TODO: might be unsafe, check later
        self.cycles_spent -= self.cycle_limit
        self.mode = state
        self.cycle_limit = state.value
    
    
    def hBlank_step(self):
        if self.cycles_spent >= self.cycle_limit:
            # move to next scanline
            self.ly = self.ly + 1

            # move to next mode 
            # >= 144 for safety, ==144 should work
            if self.ly >= 144:
                self.set_state(PPU_MODES.V_BLANK)
            else: 
                self.set_state(PPU_MODES.OAM_SCAN)
                
    def vBlank_step(self):
        if self.cycles_spent >= self.cycle_limit:
            # 10 vBlank lines are done restart from scanline 0
            self.ly += 1

        # all vBlank lines done move to OAM_SCAN for line 0
        if self.ly > 153:
            self.ly = 0
            self.set_state(PPU_MODES.OAM_SCAN)

    def step(self, cycles):
        # accumulate cycles
        self.cycles_spent = self.cycles_spent + cycles

        if self.mode == PPU_MODES.OAM_SCAN:
            pass
        elif self.mode == PPU_MODES.PIXEL_TRANSFER:
            pass
        elif self.mode == PPU_MODES.H_BLANK:
            self.hBlank_step()
        elif self.mode == PPU_MODES.V_BLANK:
            self.vBlank_step()


    def render_scanline(self):
        pass 
        
        

