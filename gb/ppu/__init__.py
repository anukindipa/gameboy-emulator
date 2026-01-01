from gb.util import PPU_MODES

class PPU():
    def __init__(self, mmu):
        # access to memory (vram, oam, etc.), shared with cpu
        self.mmu = mmu

        # initial mode is HBlank
        # set mmu ppu mode as well because cpu may read it from mmu
        # cycle limit for current mode
        self.mode = PPU_MODES.H_BLANK
        self.mmu.ppu_mode = PPU_MODES.H_BLANK
        self.cycle_limit =PPU_MODES.H_BLANK.value

        # cycles spent in current mode
        self.cycles_spent = 0  
        
        # curent_y - current scanline (0-153) also stored in LY register (0xFF44)
        # curent_x - x-coordinate of the pixel being rendered 
        self.current_y = 0
        self.current_x = 0
    
    def set_state(self, state):
        self.cycles_spent = self.cycles_spent - self.cycle_limit
        self.mode = state
        self.ppu_mode = state
        self.cycle_limit = state.value
    
    def update_LY(self):
        self.mmu.ly = self.current_y
    
    def hBlank_step(self):
        if self.cycles_spent >= self.cycle_limit:
            # move to next scanline
            self.current_y = self.current_y + 1
            self.update_LY()

            # move to next mode 
            # >= 144 for safety, ==144 should work
            if self.current_y >= 144:
                self.set_state(PPU_MODES.V_BLANK)
            else: 
                self.set_state(PPU_MODES.OAM_SCAN)
                
    def vBlank_step(self):
        if self.cycles_spent >= self.cycle_limit:
            # 10 vBlank lines are done restart from scanline 0
            self.current_y = 0
            self.update_LY()
            self.set_state(PPU_MODES.OAM_SCAN)

    def step(self, cycles):
        # accumulate cycles
        self.cycles_spent = self.cycles_spent + cycles

        if self.mode == PPU_MODES.H_BLANK:
            self.hBlank_step()
        elif self.mode == PPU_MODES.V_BLANK:
            self.vBlank_step()
        elif self.mode == PPU_MODES.OAM_SCAN:
            pass
        elif self.mode == PPU_MODES.VRAM_READ:
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

