import ctypes




MALLOCFUNC = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int32)
def malloc(iSize):
    return ctypes.addressof(ctypes.create_string_buffer(iSize))


ADL_Main_Memory_Alloc = MALLOCFUNC(malloc)
ADL = ctypes.CDLL("atiadlxy.dll")

ADL_OK = 0
ADL_DL_I2C_ACTIONREAD = 1
ADL_DL_I2C_ACTIONWRITE = 2
ADL_DL_I2C_ACTIONREAD_REPEATEDSTART = 3



class AdapterInfo(ctypes.Structure):
    _fields_ = [("iSize", ctypes.c_int),
                ("iAdapterIndex", ctypes.c_int),
                ("strUDID", ctypes.c_char * 256),
                ("iBusNumber", ctypes.c_int),
                ("iDeviceNumber", ctypes.c_int),
                ("iFunctionNumber", ctypes.c_int),
                ("iVendorNumber", ctypes.c_int),
                ("strAdapterName", ctypes.c_char * 256),
                ("strDisplayName", ctypes.c_char * 256),
                ("iPresent", ctypes.c_int),
                ("iExist", ctypes.c_int),
                ("strDriverPath", ctypes.c_char * 256),
                ("strDriverPathExt", ctypes.c_char * 256),
                ("strPNPString", ctypes.c_char * 256),
                ("iOSDisplayIndex", ctypes.c_int)]

class ADLODNParameterRange(ctypes.Structure):
    _fields_ = [("iMode", ctypes.c_int),
                ("iMin", ctypes.c_int),
                ("iMax", ctypes.c_int),
                ("iStep", ctypes.c_int),
                ("iDefault", ctypes.c_int)]


class ADLODNCapabilities(ctypes.Structure):
    _fields_ = [("iMaximumNumberOfPerformanceLevels", ctypes.c_int),
                ("sEngineClockRange", ADLODNParameterRange),
                ("sMemoryClockRange", ADLODNParameterRange),
                ("svddcRange", ADLODNParameterRange),
                ("power", ADLODNParameterRange),
                ("powerTuneTemperature", ADLODNParameterRange),
                ("fanTemperature", ADLODNParameterRange),
                ("fanSpeed", ADLODNParameterRange),
                ("minimumPerformanceClock", ADLODNParameterRange)]


class ADLODNPerformanceLevel(ctypes.Structure):
    _fields_ = [("iClock", ctypes.c_int),
                ("iVddc", ctypes.c_int),
                ("iEnabled", ctypes.c_int)]

class ADLODNPerformanceLevels(ctypes.Structure):
    _fields_ = [("iSize", ctypes.c_int),
                ("iMode", ctypes.c_int),
                ("iNumberOfPerformanceLevels", ctypes.c_int),
                ("aLevels", ADLODNPerformanceLevel * 1)]

# fake full 8 levels to make memory allocation easier with ctypes
class ADLODNPerformanceLevels8(ctypes.Structure):
    _fields_ = [("iSize", ctypes.c_int),
                ("iMode", ctypes.c_int),
                ("iNumberOfPerformanceLevels", ctypes.c_int),
                ("aLevels", ADLODNPerformanceLevel * 8)]


class ADLODNFanControl(ctypes.Structure):
    _fields_ = [("iMode", ctypes.c_int),
                ("iFanControlMode", ctypes.c_int),
                ("iCurrentFanSpeedMode", ctypes.c_int),
                ("iCurrentFanSpeed", ctypes.c_int),
                ("iTargetFanSpeed", ctypes.c_int),
                ("iTargetTemperature", ctypes.c_int),
                ("iMinPerformanceClock", ctypes.c_int),
                ("iMinFanLimit", ctypes.c_int)]



class ADLODNPowerLimitSettings(ctypes.Structure):
    _fields_ = [("iMode", ctypes.c_int),
                ("iTDPLimit", ctypes.c_int),
                ("iMaxOperatingTemperature", ctypes.c_int)]



class ADLODNPerformanceStatus(ctypes.Structure):
    _fields_ = [("iCoreClock", ctypes.c_int),
                ("iMemoryClock", ctypes.c_int),
                ("iDCEFClock", ctypes.c_int),
                ("iGFXClock", ctypes.c_int),
                ("iUVDClock", ctypes.c_int),
                ("iVCEClock", ctypes.c_int),
                ("iGPUActivityPercent", ctypes.c_int),
                ("iCurrentCorePerformanceLevel", ctypes.c_int),
                ("iCurrentMemoryPerformanceLevel", ctypes.c_int),
                ("iCurrentDCEFPerformanceLevel", ctypes.c_int),
                ("iCurrentGFXPerformanceLevel", ctypes.c_int),
                ("iUVDPerformanceLevel", ctypes.c_int),
                ("iVCEPerformanceLevel", ctypes.c_int),
                ("iCurrentBusSpeed", ctypes.c_int),
                ("iCurrentBusLanes", ctypes.c_int),
                ("iMaximumBusLanes", ctypes.c_int),
                ("iVDDC", ctypes.c_int),
                ("iVDDCI", ctypes.c_int)]


class ADLI2C(ctypes.Structure):
    _fields_ = [("iSize", ctypes.c_int),
                ("iLine", ctypes.c_int),
                ("iAddress", ctypes.c_int),
                ("iOffset", ctypes.c_int),
                ("iAction", ctypes.c_int),
                ("iSpeed", ctypes.c_int),
                ("iDataSize", ctypes.c_int),
                ("pcData", ctypes.c_char_p)]




def print_rec(t_struct, rec=0):
    for field in t_struct._fields_:
        for i in range(rec):
            print('   ', end='')

        #print(dir(getattr(t_struct, field[0])))
        if hasattr(getattr(t_struct, field[0]), '__len__'):
            #print(len(getattr(t_struct, field[0])))
            print(field[0], ':')
            for ti, t in enumerate(getattr(t_struct, field[0])):
                for i in range(rec+1):
                    print('   ', end='')
                print(ti, ":")
                print_rec(t, rec=rec+2)
        elif hasattr(getattr(t_struct, field[0]), '_fields_'):
            print(field[0], ':')
            print_rec(getattr(t_struct, field[0]), rec=rec+1)
        else:
            print(field[0], getattr(t_struct, field[0]))



class amdadl():
    def __init__(self):

        unique_cards = {}

        self.context = ctypes.c_void_p()
        if ADL_OK != ADL.ADL2_Main_Control_Create(ADL_Main_Memory_Alloc, 1, ctypes.byref(self.context)):
            print("ADL Init Error")
            exit()

        iNumAdapters = ctypes.c_int(0)
        if ADL_OK != ADL.ADL2_Adapter_NumberOfAdapters_Get(self.context, ctypes.byref(iNumAdapters)):
            print("Cannot get number of adapters!")
            exit()

        print("%d Adapters found" % iNumAdapters.value)


        infos = (iNumAdapters.value * AdapterInfo)()
        if ADL_OK != ADL.ADL2_Adapter_AdapterInfo_Get(self.context, ctypes.byref(infos), ctypes.sizeof(infos)):
            print("Cannot get number adapter infos!")
            exit()


        self.infos = infos

        # filter out actully unique cards by UDID
        # makes things easier with multi-screen setups
        for i in range(iNumAdapters.value):
            active = ctypes.c_int(0)
            if ADL_OK != ADL.ADL2_Adapter_Active_Get(self.context, i, ctypes.byref(active)):
                print("Failed to get adapter active status!")

            #print("\nAdapter %d: %s" % (i, "active" if active.value else "inactive"))

            if active.value:
                UDID = infos[i].strUDID.decode("utf-8")[0:62]
                if UDID not in unique_cards:
                    unique_cards[UDID] = i

        self.active_ids = []
        for UDID, i in unique_cards.items():
            print(UDID, len(UDID), i)
            self.active_ids.append(i)

        for UDID, i in unique_cards.items():

            print("   iAdapterIndex : %d" % (infos[i].iAdapterIndex))
            print("   strAdapterName : %s" % (infos[i].strAdapterName.decode("utf-8")))
            print("   strUDID : %s" % (infos[i].strUDID.decode("utf-8")))
            #print("   strDisplayName : %s" % (infos[i].strDisplayName.decode("utf-8")))

            iSupported = ctypes.c_int(0)
            iEnabled = ctypes.c_int(0)
            iVersion = ctypes.c_int(0)
            ADL.ADL2_Overdrive_Caps(self.context, infos[i].iAdapterIndex, ctypes.byref(iSupported), ctypes.byref(iEnabled), ctypes.byref(iVersion))

            print("   Overdrive Caps : %d %d %d" % (iSupported.value, iEnabled.value, iVersion.value))

            if iVersion.value == 7:

                overdriveCapabilities = ADLODNCapabilities()
                if ADL_OK != ADL.ADL2_OverdriveN_Capabilities_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(overdriveCapabilities)):
                    print("Failed to get Overdrive Capabilities.")
                print_rec(overdriveCapabilities, 2)


                odPerformanceLevels = ADLODNPerformanceLevels8()
                odPerformanceLevels.iSize = ctypes.sizeof(ADLODNPerformanceLevels) + ctypes.sizeof(ADLODNPerformanceLevel)*(overdriveCapabilities.iMaximumNumberOfPerformanceLevels - 1)
                odPerformanceLevels.iNumberOfPerformanceLevels = overdriveCapabilities.iMaximumNumberOfPerformanceLevels
                if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                    print("Failed to get Performance Levels.")
                print_rec(odPerformanceLevels, 2)


                odPerformanceLevelsMem = ADLODNPerformanceLevels8()
                odPerformanceLevelsMem.iSize = ctypes.sizeof(ADLODNPerformanceLevels) + ctypes.sizeof(ADLODNPerformanceLevel)*(overdriveCapabilities.iMaximumNumberOfPerformanceLevels - 1)
                odPerformanceLevelsMem.iNumberOfPerformanceLevels = overdriveCapabilities.iMaximumNumberOfPerformanceLevels
                if ADL_OK != ADL.ADL2_OverdriveN_MemoryClocks_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevelsMem)):
                    print("Failed to get Memory Performance Levels.")
                print_rec(odPerformanceLevelsMem, 2)


                odFanControl = ADLODNFanControl()
                if ADL_OK != ADL.ADL2_OverdriveN_FanControl_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(odFanControl)):
                    print("Failed to get Fan Control.")
                print_rec(odFanControl, 2)


                odPowerControl = ADLODNPowerLimitSettings()
                if ADL_OK != ADL.ADL2_OverdriveN_PowerLimit_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(odPowerControl)):
                    print("Failed to get Power Limit.")
                print_rec(odPowerControl, 2)


                odPerformanceStatus = ADLODNPerformanceStatus()
                if ADL_OK != ADL.ADL2_OverdriveN_PerformanceStatus_Get(self.context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceStatus)):
                    print("Failed to get Power Limit.")
                print_rec(odPerformanceStatus, 2)


    def I2C_read_byte(self, t_line, t_address, t_reg, t_info_id):

            pI2C = ADLI2C()
            pI2C.iSize = ctypes.sizeof(pI2C)
            pI2C.iSpeed = 100
            pI2C.iAction = ADL_DL_I2C_ACTIONREAD
            pI2C.iLine = t_line #0x04
            pI2C.iAddress = t_address << 1 #0x08 << 1
            pI2C.iOffset = t_reg #0x0D
            pI2C.iDataSize = 1

            #I2Cstore = (ctypes.c_char * 256)()
            I2Cstore = (ctypes.c_uint8 * 256)()
            pI2C.pcData = ctypes.addressof(I2Cstore)
            if ADL_OK != ADL.ADL2_Display_WriteAndReadI2C(self.context, self.infos[t_info_id].iAdapterIndex, ctypes.byref(pI2C)):
                print("Failed to read I2C.")
            #rint('%s' % I2Cstore[0].hex())
            print('I2C read byte [0x%02x 0x%02x 0x%02x] -> %02x' % (t_line, t_address, t_reg, I2Cstore[0]))
            return I2Cstore[0]


    def destroy(self):
        # clean up everything
        if ADL_OK != ADL.ADL2_Main_Control_Destroy(self.context):
            print("Failed to destroy ADL context")
            exit()
