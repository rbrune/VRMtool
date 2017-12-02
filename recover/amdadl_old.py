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




unique_cards = {}

context = ctypes.c_void_p()
if ADL_OK != ADL.ADL2_Main_Control_Create(ADL_Main_Memory_Alloc, 1, ctypes.byref(context)):
    print("ADL Init Error")
    exit()

iNumAdapters = ctypes.c_int(0)
if ADL_OK != ADL.ADL2_Adapter_NumberOfAdapters_Get(context, ctypes.byref(iNumAdapters)):
    print("Cannot get number of adapters!")
    exit()

print("%d Adapters found" % iNumAdapters.value)


infos = (iNumAdapters.value * AdapterInfo)()
if ADL_OK != ADL.ADL2_Adapter_AdapterInfo_Get(context, ctypes.byref(infos), ctypes.sizeof(infos)):
    print("Cannot get number adapter infos!")
    exit()



# filter out actully unique cards by UDID
# makes things easier with multi-screen setups
for i in range(iNumAdapters.value):
    active = ctypes.c_int(0)
    if ADL_OK != ADL.ADL2_Adapter_Active_Get(context, i, ctypes.byref(active)):
        print("Failed to get adapter active status!")

    #print("\nAdapter %d: %s" % (i, "active" if active.value else "inactive"))

    if active.value:
        UDID = infos[i].strUDID.decode("utf-8")[0:62]
        if UDID not in unique_cards:
            unique_cards[UDID] = i

for UDID, i in unique_cards.items():
    print(UDID, len(UDID), i)


for UDID, i in unique_cards.items():
    if 1:



        print("   iAdapterIndex : %d" % (infos[i].iAdapterIndex))
        print("   strAdapterName : %s" % (infos[i].strAdapterName.decode("utf-8")))
        print("   strUDID : %s" % (infos[i].strUDID.decode("utf-8")))
        #print("   strDisplayName : %s" % (infos[i].strDisplayName.decode("utf-8")))

        iSupported = ctypes.c_int(0)
        iEnabled = ctypes.c_int(0)
        iVersion = ctypes.c_int(0)
        ADL.ADL2_Overdrive_Caps(context, infos[i].iAdapterIndex, ctypes.byref(iSupported), ctypes.byref(iEnabled), ctypes.byref(iVersion))

        print("   Overdrive Caps : %d %d %d" % (iSupported.value, iEnabled.value, iVersion.value))

        if iVersion.value == 7:

            overdriveCapabilities = ADLODNCapabilities()
            if ADL_OK != ADL.ADL2_OverdriveN_Capabilities_Get(context, infos[i].iAdapterIndex, ctypes.byref(overdriveCapabilities)):
                print("Failed to get Overdrive Capabilities.")
            print_rec(overdriveCapabilities, 2)


            odPerformanceLevels = ADLODNPerformanceLevels8()
            odPerformanceLevels.iSize = ctypes.sizeof(ADLODNPerformanceLevels) + ctypes.sizeof(ADLODNPerformanceLevel)*(overdriveCapabilities.iMaximumNumberOfPerformanceLevels - 1)
            odPerformanceLevels.iNumberOfPerformanceLevels = overdriveCapabilities.iMaximumNumberOfPerformanceLevels
            if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                print("Failed to get Performance Levels.")
            print_rec(odPerformanceLevels, 2)


            odPerformanceLevelsMem = ADLODNPerformanceLevels8()
            odPerformanceLevelsMem.iSize = ctypes.sizeof(ADLODNPerformanceLevels) + ctypes.sizeof(ADLODNPerformanceLevel)*(overdriveCapabilities.iMaximumNumberOfPerformanceLevels - 1)
            odPerformanceLevelsMem.iNumberOfPerformanceLevels = overdriveCapabilities.iMaximumNumberOfPerformanceLevels
            if ADL_OK != ADL.ADL2_OverdriveN_MemoryClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevelsMem)):
                print("Failed to get Memory Performance Levels.")
            print_rec(odPerformanceLevelsMem, 2)


            odFanControl = ADLODNFanControl()
            if ADL_OK != ADL.ADL2_OverdriveN_FanControl_Get(context, infos[i].iAdapterIndex, ctypes.byref(odFanControl)):
                print("Failed to get Fan Control.")
            print_rec(odFanControl, 2)


            odPowerControl = ADLODNPowerLimitSettings()
            if ADL_OK != ADL.ADL2_OverdriveN_PowerLimit_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPowerControl)):
                print("Failed to get Power Limit.")
            print_rec(odPowerControl, 2)


            odPerformanceStatus = ADLODNPerformanceStatus()
            if ADL_OK != ADL.ADL2_OverdriveN_PerformanceStatus_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceStatus)):
                print("Failed to get Power Limit.")
            print_rec(odPerformanceStatus, 2)


            pI2C = ADLI2C()
            pI2C.iSize = ctypes.sizeof(pI2C)
            pI2C.iSpeed = 100
            pI2C.iAction = ADL_DL_I2C_ACTIONREAD
            pI2C.iLine = 0x04
            pI2C.iAddress = 0x08 << 1
            pI2C.iOffset = 0x0D
            pI2C.iDataSize = 1

            I2Cstore = (ctypes.c_char * 256)()
            pI2C.pcData = ctypes.addressof(I2Cstore)
            if ADL_OK != ADL.ADL2_Display_WriteAndReadI2C(context, infos[i].iAdapterIndex, ctypes.byref(pI2C)):
                print("Failed to read I2C.")
            print('%s' % I2Cstore[0].hex())




            pylab.ion()
            pylab.figure()

            #for iTDPLimit in range(-50, 60, 10):
            if 0:
                for iTDPLimit in [-50, -25, 0, 25, 50]:
                    print(iTDPLimit)

                    odPowerControl = ADLODNPowerLimitSettings()
                    if ADL_OK != ADL.ADL2_OverdriveN_PowerLimit_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPowerControl)):
                        print("Failed to get Power Limit.")

                    odPowerControl.iTDPLimit = iTDPLimit
                    if ADL_OK != ADL.ADL2_OverdriveN_PowerLimit_Set(context, infos[i].iAdapterIndex, ctypes.byref(odPowerControl)):
                        print("Failed to set Power Limit.")

                    perf_l = []
                    for seed in range(3):
                        print(seed)
                        perf = run_test()
                        pylab.plot(iTDPLimit, perf, 'k.')
                        perf_l.append(perf)

                        pylab.pause(0.01)
                        pylab.draw()
                        pylab.show()


                    pylab.plot(iTDPLimit, numpy.mean(perf_l), 'kx')



            if 0:
                track_clock = []
                track_perf = []

                for iClock in range(2100, 2260, 10):
                    print(iClock)

                    if ADL_OK != ADL.ADL2_OverdriveN_MemoryClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevelsMem)):
                        print("Failed to get Memory Performance Levels.")

                    odPerformanceLevelsMem.iMode = 3
                    odPerformanceLevelsMem.aLevels[1].iClock = iClock * 100

                    if ADL_OK != ADL.ADL2_OverdriveN_MemoryClocks_Set(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevelsMem)):
                        print("Failed to get Memory Performance Levels.")

                    perf_l = []
                    for seed in range(3):
                        print(seed)
                        perf = run_test()
                        pylab.plot(iClock, perf, 'k.')
                        perf_l.append(perf)

                        pylab.pause(0.01)
                        pylab.draw()
                        pylab.show()
                        if perf == 0:
                            break


                    pylab.plot(iClock, numpy.median(perf_l), 'kx')

                    track_clock.append(iClock)
                    track_perf.append(numpy.median(perf_l))

                    db = shelve.open('track.db')
                    db['track_clock'] = track_clock
                    db['track_perf'] = track_perf
                    db.close()


                    if 0 in perf_l:
                        break


            if 0:
                for iClock in reversed(range(900, 1300, 50)):
                    print(iClock)

                    if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                        print("Failed to get Memory GPU Levels.")

                    odPerformanceLevels.iMode = 3
                    odPerformanceLevels.aLevels[7].iClock = iClock * 100

                    if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Set(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                        print("Failed to set GPU performance Levels.")

                    perf_l = []
                    for seed in range(1):
                        print(seed)
                        perf = run_test()
                        pylab.plot(iClock, perf, 'k.')
                        perf_l.append(perf)

                        pylab.pause(0.01)
                        pylab.draw()
                        pylab.show()


                    pylab.plot(iClock, numpy.mean(perf_l), 'kx')

            if 0:
                iClock = 1100
                print(iClock)

                if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                    print("Failed to get Memory GPU Levels.")

                odPerformanceLevels.iMode = 3
                odPerformanceLevels.aLevels[6].iClock = 1000 * 100
                odPerformanceLevels.aLevels[6].iVddc = 1100

                odPerformanceLevels.aLevels[7].iClock = 1100 * 100
                odPerformanceLevels.aLevels[7].iVddc = 1050

                print_rec(odPerformanceLevels, 2)

                if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Set(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                    print("Failed to set GPU performance Levels.")

                if ADL_OK != ADL.ADL2_OverdriveN_SystemClocks_Get(context, infos[i].iAdapterIndex, ctypes.byref(odPerformanceLevels)):
                    print("Failed to get Memory GPU Levels.")

                print_rec(odPerformanceLevels, 2)

                #pylab.pause(0.01)
                #pylab.draw()
                #pylab.show()




# clean up everything
if ADL_OK != ADL.ADL2_Main_Control_Destroy(context):
    print("Failed to destroy ADL context")
    exit()

pylab.ioff()
pylab.show()
