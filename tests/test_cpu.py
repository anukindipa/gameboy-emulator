import pytest
from gb.cpu.registers import Registers


@pytest.fixture
def registers():
    return Registers()


@pytest.mark.parametrize("reg_xy", ["AF", "BC", "DE", "HL"])
def test_register_get_set_ind_first(registers, reg_xy):
    # set reg x and reg y individually and read xy
    reg_x = reg_xy[0]
    reg_y = reg_xy[1]

    setattr(registers, reg_x, 0xAB)
    setattr(registers, reg_y, 0xCD)
    assert getattr(registers, reg_xy) == 0xABCD


@pytest.mark.parametrize("reg_xy", ["AF", "BC", "DE", "HL"])
def test_register_get_set_pair_first(registers, reg_xy):
    # set reg xy and see if reg x and reg y are updated
    reg_x = reg_xy[0]
    reg_y = reg_xy[1]

    setattr(registers, reg_xy, 0x1234)

    # test if if individual registers were updated
    assert getattr(registers, reg_x) == 0x12
    assert getattr(registers, reg_y) == 0x34


def read_register(register_obj, register_name):
    """helper function used in test_register_get_custom_funcs
    sees if registers.XY returns the value of register XY"""
    # pair registers
    if register_name == "AF":
        return register_obj.AF 
    if register_name == "BC":
        return register_obj.BC
    if register_name == "DE":
        return register_obj.DE
    if register_name == "HL":
        return register_obj.HL


@pytest.mark.parametrize("reg_xy", ["AF", "BC", "DE", "HL"])
def test_register_get_custom_funcs(registers, reg_xy):
    """test if functions with and @property for reading values work properly"""
    reg_x = reg_xy[0]
    reg_y = reg_xy[1]

    # set reg x and reg y individually and read xy
    # no need to test if statements for single registers like 
    # registers.A are valid as single registers are already attributes
    setattr(registers, reg_x, 0xAB)
    setattr(registers, reg_y, 0xCD)

    # test if @property for registers like AF work properly
    assert getattr(registers, reg_xy) == read_register(registers, reg_xy)
    assert read_register(registers, reg_xy) == 0xABCD


def set_register(register_obj, register_name, val):
    """helper function used in test_register_set_custom_funcs
    used to see if functions with @XY.setter work properly"""
    if register_name == "AF":
        register_obj.AF = val
    if register_name == "BC":
        register_obj.BC = val
    if register_name == "DE":
        register_obj.DE = val
    if register_name == "HL":
        register_obj.HL = val

@pytest.mark.parametrize("reg_xy", ["AF", "BC", "DE", "HL"])
def test_register_set_custom_funcs(registers, reg_xy):
    """test if functions with @XY.setter for setting values work properly"""

    # test setting functions
    set_register(registers, reg_xy, 0x1234)

    # test if correct value was written
    assert getattr(registers, reg_xy) == 0x1234

def test_PC_SP(registers):
    # test PC and SP registers
    assert getattr(registers, "PC") == 0
    registers.PC += 1
    assert getattr(registers, "PC") == 1
    assert getattr(registers, "SP") == 0
    registers.SP += 1
    assert getattr(registers, "SP") == 1
