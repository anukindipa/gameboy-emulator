def interrupt_handler(cpu):
    """Handles any pending interrupts."""
    memory = cpu.mmu

    # Read the interrupt enable and flag registers
    IE = memory.read_byte(0xFFFF)
    IF = memory.read_byte(0xFF0F)

    # Check for any pending interrupt (even if IME=0, HALT can exit)
    has_pending_interrupt = (IE & IF) != 0

    # If halted and there's a pending interrupt, exit HALT
    # (hardware always wakes from HALT on any pending interrupt)
    if cpu.halted and has_pending_interrupt:
        cpu.halted = False
        # If IME=0, we exit HALT but don't service the interrupt
        # This is the HALT bug behavior
        if not cpu.ime:
            return 0

    # Service interrupt only if IME is enabled
    if not cpu.ime:
        return 0

    # Check for each interrupt in order of priority
    for i in range(5):
        interrupt_bit = 1 << i
        if (IE & interrupt_bit) and (IF & interrupt_bit):
            interrupt_names = ["V-Blank", "LCD STAT", "Timer", "Serial", "Joypad"]
            
            # Clear the interrupt flag
            memory.write_byte(0xFF0F, IF & ~interrupt_bit)

            # Disable IME
            cpu.ime = False

            # Disable halt
            cpu.halted = False

            # Push current PC onto stack
            pc = cpu.registers.PC
            cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
            cpu.write_d8(cpu.registers.SP, (pc >> 8) & 0xFF)
            cpu.registers.SP = (cpu.registers.SP - 1) & 0xFFFF
            cpu.write_d8(cpu.registers.SP, pc & 0xFF)

            # Jump to the interrupt vector
            cpu.registers.PC = 0x40 + (i * 8)

            # Interrupt takes 5 machine cycles (20 clock cycles)
            return 20

    return 0  # No interrupts serviced