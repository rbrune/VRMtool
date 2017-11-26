import ctypes
import struct









# https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/include/asic_reg/smu/smu_7_1_3_d.h
# https://cgit.freedesktop.org/amd/umr/tree/src/lib/ip/smu713_bits.i


# actual address is register * 4
mmSMC_MESSAGE_0 = 0x94
mmSMC_MESSAGE_1 = 0x96

mmSMC_RESP_0 = 0x95
mmSMC_RESP_1 = 0x97

mmSMC_MSG_ARG_0 = 0xa4
mmSMC_MSG_ARG_1 = 0xa5

mmSMC_IND_INDEX_0 = 0x80
mmSMC_IND_INDEX_1 = 0x82

mmSMC_IND_DATA_0 = 0x81
mmSMC_IND_DATA_1 = 0x83



# Miscellaneous
FDO_PWM_MODE_STATIC = 0x1
FDO_PWM_MODE_STATIC_RPM = 0x5


# indirect register access through SMC
ixCG_THERMAL_STATUS = 0xc0300008
ixCG_TACH_STATUS = 0xc0300074
ixCG_FDO_CTRL0 = 0xc0300064
ixCG_FDO_CTRL1 = 0xc0300068
ixCG_FDO_CTRL2 = 0xc030006c



class ixCG_THERMAL_STATUS_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("SPARE", ctypes.c_uint32, 8),
        ("FDO_PWM_DUTY", ctypes.c_uint32, 8),
        ("THERM_ALERT", ctypes.c_uint32, 1),
        ("GEN_STATUS", ctypes.c_uint32, 4)
    ]
class ixCG_THERMAL_STATUS_Pack(ctypes.Union):
    _fields_ = [("bits", ixCG_THERMAL_STATUS_PackBits),
                ("binary_data", ctypes.c_uint32)]





class ixCG_FDO_CTRL0_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("FDO_STATIC_DUTY", ctypes.c_uint32, 8),
        ("FAN_SPINUP_DUTY", ctypes.c_uint32, 8),
        ("FDO_PWM_MANUAL", ctypes.c_uint32, 1),
        ("FDO_PWM_HYSTER", ctypes.c_uint32, 6),
        ("FDO_PWM_RAMP_EN", ctypes.c_uint32, 1),
        ("FDO_PWM_RAMP", ctypes.c_uint32, 8)
    ]
class ixCG_FDO_CTRL0_Pack(ctypes.Union):
    _fields_ = [("bits", ixCG_FDO_CTRL0_PackBits),
                ("binary_data", ctypes.c_uint32)]



class ixCG_FDO_CTRL1_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("FMAX_DUTY100", ctypes.c_uint32, 8),
        ("FMIN_DUTY", ctypes.c_uint32, 8),
        ("M", ctypes.c_uint32, 8),
        ("RESERVED", ctypes.c_uint32, 6),
        ("FDO_PWRDNB", ctypes.c_uint32, 1)
    ]
class ixCG_FDO_CTRL1_Pack(ctypes.Union):
    _fields_ = [("bits", ixCG_FDO_CTRL1_PackBits),
                ("binary_data", ctypes.c_uint32)]


class ixCG_FDO_CTRL2_PackBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("TMIN", ctypes.c_uint32, 8),
        ("FAN_SPINUP_TIME", ctypes.c_uint32, 3),
        ("FDO_PWM_MODE", ctypes.c_uint32, 3),
        ("TMIN_HYSTER", ctypes.c_uint32, 3),
        ("TMAX", ctypes.c_uint32, 8),
        ("TACH_PWM_RESP_RATE", ctypes.c_uint32, 7)
    ]
class ixCG_FDO_CTRL2_Pack(ctypes.Union):
    _fields_ = [("bits", ixCG_FDO_CTRL2_PackBits),
                ("binary_data", ctypes.c_uint32)]
