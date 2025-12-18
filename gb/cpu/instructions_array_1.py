################################################################################
# behavior reference:
#   https://gbdev.io/pandocs/CPU_Instruction_Set.html
#   https://rgbds.gbdev.io/docs/v1.0.0/gbz80.7#POP_r16
#   https://gekkio.fi/files/gb-docs/gbctr.pdf
# optable:
#   https://gbdev.io/gb-opcodes/optables/
################################################################################
# r8 is a normal register like A, B
# r16 is a 'pair' register like DE, HL
# d16 is a 16 bit value
################################################################################

from gb.cpu.instructions_funcs_1_Arithmetic import *
from gb.cpu.instructions_funcs_1_Bitwise_logic import *
from gb.cpu.instructions_funcs_1_LD import *
from gb.cpu.instructions_funcs_1_Misc import *
from gb.cpu.instructions_funcs_1_Stack import *

def construct_code_array():
    """
    maps opcode numbers to functions implementing them.
    see relevant files for function implementations.
    """

    code_arr = [None] * 256

    # 0x00..0x0f
    code_arr[0x00] = NOP
    code_arr[0x01] = lambda cpu: LD_r16_d16(cpu, "BC")
    code_arr[0x02] = lambda cpu: LD_m8_r8(cpu, "BC", "A")
    code_arr[0x03] = lambda cpu: INC_r16(cpu, "BC")
    code_arr[0x04] = lambda cpu: INC_r8(cpu, "B")
    code_arr[0x05] = lambda cpu: DEC_r8(cpu, "B")
    code_arr[0x06] = lambda cpu: LD_r8_d8(cpu, "B")
    #
    #
    code_arr[0x0a] = lambda cpu: LD_r8_m8(cpu, "A", "BC")
    code_arr[0x0b] = lambda cpu: DEC_r16(cpu, "BC")
    code_arr[0x0c] = lambda cpu: INC_r8(cpu, "C")
    code_arr[0x0d] = lambda cpu: DEC_r8(cpu, "C")
    code_arr[0x0e] = lambda cpu: LD_r8_d8(cpu, "C")
    #

    # 0x10..0x1f
    code_arr[0x11] = lambda cpu: LD_r16_d16(cpu, "DE")
    code_arr[0x12] = lambda cpu: LD_m8_r8(cpu, "DE", "A")
    code_arr[0x13] = lambda cpu: INC_r16(cpu, "DE")
    code_arr[0x14] = lambda cpu: INC_r8(cpu, "D")
    code_arr[0x15] = lambda cpu: DEC_r8(cpu, "D")
    code_arr[0x16] = lambda cpu: LD_r8_d8(cpu, "D")
    #
    #
    code_arr[0x1a] = lambda cpu: LD_r8_m8(cpu, "A", "DE")
    code_arr[0x1b] = lambda cpu: DEC_r16(cpu, "DE")
    code_arr[0x1c] = lambda cpu: INC_r8(cpu, "E")
    code_arr[0x1d] = lambda cpu: DEC_r8(cpu, "E")
    code_arr[0x1e] = lambda cpu: LD_r8_d8(cpu, "E")
    #

    # 0x20..0x2f
    code_arr[0x21] = lambda cpu: LD_r16_d16(cpu, "HL")
    code_arr[0x22] = lambda cpu: LD_HLID_A(cpu, increment=True)
    code_arr[0x23] = lambda cpu: INC_r16(cpu, "HL")
    code_arr[0x24] = lambda cpu: INC_r8(cpu, "H")
    code_arr[0x25] = lambda cpu: DEC_r8(cpu, "H")
    code_arr[0x26] = lambda cpu: LD_r8_d8(cpu, "H")
    #
    #
    code_arr[0x2a] = lambda cpu: LD_A_HLID(cpu, increment=True)
    code_arr[0x2b] = lambda cpu: DEC_r16(cpu, "HL")
    code_arr[0x2c] = lambda cpu: INC_r8(cpu, "L")
    code_arr[0x2d] = lambda cpu: DEC_r8(cpu, "L")
    code_arr[0x2e] = lambda cpu: LD_r8_d8(cpu, "L")
    #

    # 0x30..0x3f
    code_arr[0x31] = lambda cpu: LD_r16_d16(cpu, "SP")
    code_arr[0x32] = lambda cpu: LD_HLID_A(cpu, increment=False)
    code_arr[0x33] = lambda cpu: INC_r16(cpu, "SP")
    code_arr[0x34] = lambda cpu: INC_r8(cpu, None, HL=True)
    code_arr[0x35] = lambda cpu: DEC_r8(cpu, None, HL=True)
    code_arr[0x36] = lambda cpu: LD_m8_d8(cpu, "HL")
    #
    #
    code_arr[0x3a] = lambda cpu: LD_A_HLID(cpu, increment=False)
    code_arr[0x3b] = lambda cpu: DEC_r16(cpu, "SP")
    code_arr[0x3c] = lambda cpu: INC_r8(cpu, "A")
    code_arr[0x3d] = lambda cpu: DEC_r8(cpu, "A")
    code_arr[0x3e] = lambda cpu: LD_r8_d8(cpu, "A")
    #

    # 0x40..0x4f
    code_arr[0x40] = lambda cpu: LD_r8_r8(cpu, "B", "B")
    code_arr[0x41] = lambda cpu: LD_r8_r8(cpu, "B", "C")
    code_arr[0x42] = lambda cpu: LD_r8_r8(cpu, "B", "D")
    code_arr[0x43] = lambda cpu: LD_r8_r8(cpu, "B", "E")
    code_arr[0x44] = lambda cpu: LD_r8_r8(cpu, "B", "H")
    code_arr[0x45] = lambda cpu: LD_r8_r8(cpu, "B", "L")
    code_arr[0x46] = lambda cpu: LD_r8_m8(cpu, "B", "HL")
    code_arr[0x47] = lambda cpu: LD_r8_r8(cpu, "B", "A")
    code_arr[0x48] = lambda cpu: LD_r8_r8(cpu, "C", "B")
    code_arr[0x49] = lambda cpu: LD_r8_r8(cpu, "C", "C")
    code_arr[0x4a] = lambda cpu: LD_r8_r8(cpu, "C", "D")
    code_arr[0x4b] = lambda cpu: LD_r8_r8(cpu, "C", "E")
    code_arr[0x4c] = lambda cpu: LD_r8_r8(cpu, "C", "H")
    code_arr[0x4d] = lambda cpu: LD_r8_r8(cpu, "C", "L")
    code_arr[0x4e] = lambda cpu: LD_r8_m8(cpu, "C", "HL")
    code_arr[0x4f] = lambda cpu: LD_r8_r8(cpu, "C", "A")

    # 0x50..0x5f
    code_arr[0x50] = lambda cpu: LD_r8_r8(cpu, "D", "B")
    code_arr[0x51] = lambda cpu: LD_r8_r8(cpu, "D", "C")
    code_arr[0x52] = lambda cpu: LD_r8_r8(cpu, "D", "D")
    code_arr[0x53] = lambda cpu: LD_r8_r8(cpu, "D", "E")
    code_arr[0x54] = lambda cpu: LD_r8_r8(cpu, "D", "H")
    code_arr[0x55] = lambda cpu: LD_r8_r8(cpu, "D", "L")
    code_arr[0x56] = lambda cpu: LD_r8_m8(cpu, "D", "HL")
    code_arr[0x57] = lambda cpu: LD_r8_r8(cpu, "D", "A")
    code_arr[0x58] = lambda cpu: LD_r8_r8(cpu, "E", "B")
    code_arr[0x59] = lambda cpu: LD_r8_r8(cpu, "E", "C")
    code_arr[0x5a] = lambda cpu: LD_r8_r8(cpu, "E", "D")
    code_arr[0x5b] = lambda cpu: LD_r8_r8(cpu, "E", "E")
    code_arr[0x5c] = lambda cpu: LD_r8_r8(cpu, "E", "H")
    code_arr[0x5d] = lambda cpu: LD_r8_r8(cpu, "E", "L")
    code_arr[0x5e] = lambda cpu: LD_r8_m8(cpu, "E", "HL")
    code_arr[0x5f] = lambda cpu: LD_r8_r8(cpu, "E", "A")

    # 0x60..0x6f
    code_arr[0x60] = lambda cpu: LD_r8_r8(cpu, "H", "B")
    code_arr[0x61] = lambda cpu: LD_r8_r8(cpu, "H", "C")
    code_arr[0x62] = lambda cpu: LD_r8_r8(cpu, "H", "D")
    code_arr[0x63] = lambda cpu: LD_r8_r8(cpu, "H", "E")
    code_arr[0x64] = lambda cpu: LD_r8_r8(cpu, "H", "H")
    code_arr[0x65] = lambda cpu: LD_r8_r8(cpu, "H", "L")
    code_arr[0x56] = lambda cpu: LD_r8_m8(cpu, "H", "HL")
    code_arr[0x67] = lambda cpu: LD_r8_r8(cpu, "H", "A")
    code_arr[0x68] = lambda cpu: LD_r8_r8(cpu, "L", "B")
    code_arr[0x69] = lambda cpu: LD_r8_r8(cpu, "L", "C")
    code_arr[0x6a] = lambda cpu: LD_r8_r8(cpu, "L", "D")
    code_arr[0x6b] = lambda cpu: LD_r8_r8(cpu, "L", "E")
    code_arr[0x6c] = lambda cpu: LD_r8_r8(cpu, "L", "H")
    code_arr[0x6d] = lambda cpu: LD_r8_r8(cpu, "L", "L")
    code_arr[0x6e] = lambda cpu: LD_r8_m8(cpu, "L", "HL")
    code_arr[0x6f] = lambda cpu: LD_r8_r8(cpu, "L", "A")

    # 0x70..0x7f
    code_arr[0x70] = lambda cpu: LD_m8_r8(cpu, "HL", "B")
    code_arr[0x71] = lambda cpu: LD_m8_r8(cpu, "HL", "C")
    code_arr[0x72] = lambda cpu: LD_m8_r8(cpu, "HL", "D")
    code_arr[0x73] = lambda cpu: LD_m8_r8(cpu, "HL", "E")
    code_arr[0x74] = lambda cpu: LD_m8_r8(cpu, "HL", "H")
    code_arr[0x75] = lambda cpu: LD_m8_r8(cpu, "HL", "L")
    #
    code_arr[0x77] = lambda cpu: LD_m8_r8(cpu, "HL", "A")
    #
    code_arr[0x78] = lambda cpu: LD_r8_r8(cpu, "A", "B")
    code_arr[0x79] = lambda cpu: LD_r8_r8(cpu, "A", "C")
    code_arr[0x7a] = lambda cpu: LD_r8_r8(cpu, "A", "D")
    code_arr[0x7b] = lambda cpu: LD_r8_r8(cpu, "A", "E")
    code_arr[0x7c] = lambda cpu: LD_r8_r8(cpu, "A", "H")
    code_arr[0x7d] = lambda cpu: LD_r8_r8(cpu, "A", "L")
    code_arr[0x7e] = lambda cpu: LD_r8_m8(cpu, "A", "HL")
    code_arr[0x7f] = lambda cpu: LD_r8_r8(cpu, "A", "A")

    # 0x80..0x8f 
    code_arr[0x80] = lambda cpu: ADD_A_r8(cpu, "B")
    code_arr[0x81] = lambda cpu: ADD_A_r8(cpu, "C")
    code_arr[0x82] = lambda cpu: ADD_A_r8(cpu, "D")
    code_arr[0x83] = lambda cpu: ADD_A_r8(cpu, "E")
    code_arr[0x84] = lambda cpu: ADD_A_r8(cpu, "H")
    code_arr[0x85] = lambda cpu: ADD_A_r8(cpu, "L")
    code_arr[0x86] = lambda cpu: ADD_A_r8(cpu, None, HL=True)
    code_arr[0x87] = lambda cpu: ADD_A_r8(cpu, "A")
    code_arr[0x88] = lambda cpu: ADC_A_r8(cpu, "B")
    code_arr[0x89] = lambda cpu: ADC_A_r8(cpu, "C")
    code_arr[0x8a] = lambda cpu: ADC_A_r8(cpu, "D")
    code_arr[0x8b] = lambda cpu: ADC_A_r8(cpu, "E")
    code_arr[0x8c] = lambda cpu: ADC_A_r8(cpu, "H")
    code_arr[0x8d] = lambda cpu: ADC_A_r8(cpu, "L")
    code_arr[0x8e] = lambda cpu: ADC_A_r8(cpu, None, HL=True)
    code_arr[0x8f] = lambda cpu: ADC_A_r8(cpu, "A")

    # 0x90..0x9f 
    code_arr[0x90] = lambda cpu: SUB_A_r8(cpu, "B")
    code_arr[0x91] = lambda cpu: SUB_A_r8(cpu, "C")
    code_arr[0x92] = lambda cpu: SUB_A_r8(cpu, "D")
    code_arr[0x93] = lambda cpu: SUB_A_r8(cpu, "E")
    code_arr[0x94] = lambda cpu: SUB_A_r8(cpu, "H")
    code_arr[0x95] = lambda cpu: SUB_A_r8(cpu, "L")
    code_arr[0x96] = lambda cpu: SUB_A_r8(cpu, None, HL=True)
    code_arr[0x97] = lambda cpu: SUB_A_r8(cpu, "A")
    code_arr[0x98] = lambda cpu: SBC_A_r8(cpu, "B")
    code_arr[0x99] = lambda cpu: SBC_A_r8(cpu, "C")
    code_arr[0x9a] = lambda cpu: SBC_A_r8(cpu, "D")
    code_arr[0x9b] = lambda cpu: SBC_A_r8(cpu, "E")
    code_arr[0x9c] = lambda cpu: SBC_A_r8(cpu, "H")
    code_arr[0x9d] = lambda cpu: SBC_A_r8(cpu, "L")
    code_arr[0x9e] = lambda cpu: SBC_A_r8(cpu, None, HL=True)
    code_arr[0x9f] = lambda cpu: SBC_A_r8(cpu, "A")

    # 0xa0..0xaf 
    code_arr[0xa0] = lambda cpu: AND_A_r8(cpu, "B")
    code_arr[0xa1] = lambda cpu: AND_A_r8(cpu, "C")
    code_arr[0xa2] = lambda cpu: AND_A_r8(cpu, "D")
    code_arr[0xa3] = lambda cpu: AND_A_r8(cpu, "E")
    code_arr[0xa4] = lambda cpu: AND_A_r8(cpu, "H")
    code_arr[0xa5] = lambda cpu: AND_A_r8(cpu, "L")
    code_arr[0xa6] = lambda cpu: AND_A_r8(cpu, None, HL=True)
    code_arr[0xa7] = lambda cpu: AND_A_r8(cpu, "A")
    code_arr[0xa8] = lambda cpu: XOR_A_r8(cpu, "B")
    code_arr[0xa9] = lambda cpu: XOR_A_r8(cpu, "C")
    code_arr[0xaa] = lambda cpu: XOR_A_r8(cpu, "D")
    code_arr[0xab] = lambda cpu: XOR_A_r8(cpu, "E")
    code_arr[0xac] = lambda cpu: XOR_A_r8(cpu, "H")
    code_arr[0xad] = lambda cpu: XOR_A_r8(cpu, "L")
    code_arr[0xae] = lambda cpu: XOR_A_r8(cpu, None, HL=True)
    code_arr[0xaf] = lambda cpu: XOR_A_r8(cpu, "A")

    # 0xb0..0xbf 
    code_arr[0xb0] = lambda cpu: OR_A_r8(cpu, "B")
    code_arr[0xb1] = lambda cpu: OR_A_r8(cpu, "C")
    code_arr[0xb2] = lambda cpu: OR_A_r8(cpu, "D")
    code_arr[0xb3] = lambda cpu: OR_A_r8(cpu, "E")
    code_arr[0xb4] = lambda cpu: OR_A_r8(cpu, "H")
    code_arr[0xb5] = lambda cpu: OR_A_r8(cpu, "L")
    code_arr[0xb6] = lambda cpu: OR_A_r8(cpu, None, HL=True)
    code_arr[0xb7] = lambda cpu: OR_A_r8(cpu, "A")
    code_arr[0xb8] = lambda cpu: CP_A_r8(cpu, "B")
    code_arr[0xb9] = lambda cpu: CP_A_r8(cpu, "C")
    code_arr[0xba] = lambda cpu: CP_A_r8(cpu, "D")
    code_arr[0xbb] = lambda cpu: CP_A_r8(cpu, "E")
    code_arr[0xbc] = lambda cpu: CP_A_r8(cpu, "H")
    code_arr[0xbd] = lambda cpu: CP_A_r8(cpu, "L")
    code_arr[0xbe] = lambda cpu: CP_A_r8(cpu, None, HL=True)
    code_arr[0xbf] = lambda cpu: CP_A_r8(cpu, "A")



    # 0xe0..0xef
    code_arr[0xe0] = lambda cpu: LD_d8_A(cpu)
    #
    code_arr[0xe2] = lambda cpu: LDH_C_A(cpu)
    #
    #
    code_arr[0xea] = lambda cpu: LD_d16_A(cpu)
    #
    #

    # 0xf0..0xff
    code_arr[0xf0] = lambda cpu: LD_A_d8(cpu)
    #
    code_arr[0xf2] = lambda cpu: LDH_A_C(cpu)
    #
    #
    code_arr[0xfa] = lambda cpu: LD_A_d16(cpu)
    #
    #

    return code_arr
