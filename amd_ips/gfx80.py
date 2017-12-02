import ctypes
import struct









# https://cgit.freedesktop.org/amd/umr/tree/src/lib/ip/gfx80_regs.i
# https://cgit.freedesktop.org/amd/umr/tree/src/lib/ip/gfx80_bits.i


# actual address is register * 4
mmSQC_EDC_CNT = 0x23a0


class mmSQC_EDC_CNT_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("INST_SEC", ctypes.c_uint32, 8),
        ("INST_DED", ctypes.c_uint32, 8),
        ("DATA_SEC", ctypes.c_uint32, 8),
        ("DATA_DED", ctypes.c_uint32, 8),
        ]
class mmSQC_EDC_CNT_Pack(ctypes.Union):
    _fields_ = [("bits", mmSQC_EDC_CNT_PackBits),
                ("binary_data", ctypes.c_uint32)]
