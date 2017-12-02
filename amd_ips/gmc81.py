import ctypes
import struct









# https://cgit.freedesktop.org/amd/umr/tree/src/lib/ip/gmc81_regs.i
# https://cgit.freedesktop.org/amd/umr/tree/src/lib/ip/gmc81_bits.i


# actual address is register * 4
mmMC_ARB_GECC2_STATUS = 0x9c2

mmMC_SEQ_RAS_TIMING = 0xa28
mmMC_SEQ_CAS_TIMING = 0xa29
mmMC_SEQ_MISC_TIMING = 0xa2a
mmMC_SEQ_MISC_TIMING2 = 0xa2b

mmMC_ARB_DRAM_TIMING = 0x9dd
mmMC_ARB_DRAM_TIMING2 = 0x9de


class mmMC_SEQ_CAS_TIMING_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("TNOPW", ctypes.c_uint32, 2),
        ("TNOPR", ctypes.c_uint32, 2),
        ("TR2W", ctypes.c_uint32, 5),
        ("TCCDL", ctypes.c_uint32, 3),
        ("TR2R", ctypes.c_uint32, 4),
        ("TW2R", ctypes.c_uint32, 5),
        ("padding0", ctypes.c_uint32, 3),
        ("TCL", ctypes.c_uint32, 5),
        ]
class mmMC_SEQ_CAS_TIMING_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_SEQ_CAS_TIMING_PackBits),
                ("binary_data", ctypes.c_uint32)]


class mmMC_SEQ_RAS_TIMING_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("TRCDW", ctypes.c_uint32, 5),
        ("TRCDWA", ctypes.c_uint32, 5),
        ("TRCDR", ctypes.c_uint32, 5),
        ("TRCDRA", ctypes.c_uint32, 5),
        ("TRRD", ctypes.c_uint32, 4),
        ("TRC", ctypes.c_uint32, 7),
        ]
class mmMC_SEQ_RAS_TIMING_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_SEQ_RAS_TIMING_PackBits),
                ("binary_data", ctypes.c_uint32)]


class mmMC_SEQ_MISC_TIMING_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("TRP_WRA", ctypes.c_uint32, 6),
        ("padding0", ctypes.c_uint32, 2),
        ("TRP_RDA", ctypes.c_uint32, 6),
        ("padding1", ctypes.c_uint32, 1),
        ("TRP", ctypes.c_uint32, 5),
        ("TRFC", ctypes.c_uint32, 9),
        ]
class mmMC_SEQ_MISC_TIMING_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_SEQ_MISC_TIMING_PackBits),
                ("binary_data", ctypes.c_uint32)]


class mmMC_SEQ_MISC_TIMING2_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("PA2RDATA", ctypes.c_uint32, 3),
        ("padding0", ctypes.c_uint32, 1),
        ("PA2WDATA", ctypes.c_uint32, 3),
        ("padding1", ctypes.c_uint32, 1),
        ("FAW", ctypes.c_uint32, 5),
        ("TREDC", ctypes.c_uint32, 3),
        ("TWEDC", ctypes.c_uint32, 5),
        ("T32AW", ctypes.c_uint32, 4),
        ("padding2", ctypes.c_uint32, 3),
        ("TWDATATR", ctypes.c_uint32, 4),
        ]
class mmMC_SEQ_MISC_TIMING2_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_SEQ_MISC_TIMING2_PackBits),
                ("binary_data", ctypes.c_uint32)]



class mmMC_ARB_DRAM_TIMING_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ACTRD", ctypes.c_uint32, 8),
        ("ACTWR", ctypes.c_uint32, 8),
        ("RASMACTRD", ctypes.c_uint32, 8),
        ("RASMACTWR", ctypes.c_uint32, 8),
        ]
class mmMC_ARB_DRAM_TIMING_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_ARB_DRAM_TIMING_PackBits),
                ("binary_data", ctypes.c_uint32)]


class mmMC_ARB_DRAM_TIMING2_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("RAS2RAS", ctypes.c_uint32, 8),
        ("RP", ctypes.c_uint32, 8),
        ("WRPLUSRP", ctypes.c_uint32, 8),
        ("BUS_TURN", ctypes.c_uint32, 5),
        ]
class mmMC_ARB_DRAM_TIMING2_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_ARB_DRAM_TIMING2_PackBits),
                ("binary_data", ctypes.c_uint32)]








class mmMC_ARB_GECC2_STATUS_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("CORR_STS0", ctypes.c_uint32, 1),
        ("UNCORR_STS0", ctypes.c_uint32, 1),
        ("FED_STS0", ctypes.c_uint32, 1),
        ("RSVD0", ctypes.c_uint32, 1),
        ("CORR_STS1", ctypes.c_uint32, 1),
        ("UNCORR_STS1", ctypes.c_uint32, 1),
        ("FED_STS1", ctypes.c_uint32, 1),
        ("RSVD1", ctypes.c_uint32, 1),
        ("CORR_CLEAR0", ctypes.c_uint32, 1),
        ("UNCORR_CLEAR0", ctypes.c_uint32, 1),
        ("FED_CLEAR0", ctypes.c_uint32, 1),
        ("RSVD2", ctypes.c_uint32, 1),
        ("CORR_CLEAR1", ctypes.c_uint32, 1),
        ("UNCORR_CLEAR1", ctypes.c_uint32, 1),
        ("FED_CLEAR1", ctypes.c_uint32, 1),
        ("RSVD3", ctypes.c_uint32, 1),
        ("RMWRD_CORR_STS0", ctypes.c_uint32, 1),
        ("RMWRD_UNCORR_STS0", ctypes.c_uint32, 1),
        ("RSVD4", ctypes.c_uint32, 1),
        ("RMWRD_CORR_STS1", ctypes.c_uint32, 1),
        ("RMWRD_UNCORR_STS1", ctypes.c_uint32, 1),
        ("RSVD5", ctypes.c_uint32, 1),
        ("RMWRD_CORR_CLEAR0", ctypes.c_uint32, 1),
        ("RMWRD_UNCORR_CLEAR0", ctypes.c_uint32, 1),
        ("RSVD6", ctypes.c_uint32, 1),
        ("RMWRD_CORR_CLEAR1", ctypes.c_uint32, 1),
        ("RMWRD_UNCORR_CLEAR1", ctypes.c_uint32, 1),
        ]
class mmMC_ARB_GECC2_STATUS_Pack(ctypes.Union):
    _fields_ = [("bits", mmMC_ARB_GECC2_STATUS_PackBits),
                ("binary_data", ctypes.c_uint32)]
