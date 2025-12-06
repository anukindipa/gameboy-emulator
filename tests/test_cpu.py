import pytest
from gb.cpu.registers import Registers

@pytest.fixture
def registers():
    return Registers()

def test_register_get_set(registers):
    for reg_xy in ("AF", "BC", "DE", "HL"):
        reg_x = reg_xy[0]
        reg_y = reg_xy[1]

        # set reg x and reg y individually and read xy
        setattr(registers, reg_x, 0xAB)
        setattr(registers, reg_y, 0xCD)
        assert getattr(registers, reg_xy) == 0xABCD

    for reg_xy in ("AF", "BC", "DE", "HL"):
        reg_x = reg_xy[0]
        reg_y = reg_xy[1]

        # set reg xy and see if reg x and reg y are updated
        setattr(registers, reg_xy, 0x1234)
        # test if xy was updated properly
        assert getattr(registers, reg_xy) == 0x1234
        # test if if individual registers were updated
        assert getattr(registers, reg_x) == 0x12
        assert getattr(registers, reg_y) == 0x34

def test_PC_SP(registers):
    # test PC and SP registers
    assert getattr(registers, "PC") == 0
    registers.PC += 1
    assert getattr(registers, "PC") == 1
    assert getattr(registers, "SP") == 0
    registers.SP += 1
    assert getattr(registers, "SP") == 1
