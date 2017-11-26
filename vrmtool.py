import ctypes
import struct
import os
import sys
import time

import tkinter as tk

import exeio
import polaris10


# fix bad font rendering on screens with high dpi scaling activated
ctypes.windll.shcore.SetProcessDpiAwareness(1)

iomap = exeio.exeio()

gpus = []
gpus.append(polaris10.polaris10(iomap, 0))


root = tk.Tk()
#root.resizable(0,0)

class App:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()
        self.frame = frame

        self.et = tk.StringVar()
        self.entry = tk.Entry(frame, textvariable = self.et)
        self.entry.pack(side=tk.LEFT)

        self.button = tk.Button(frame, text="QUIT", fg="red", command=quit)
        self.button.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame, text="Hello", command=self.write_slogan)
        self.slogan.pack(side=tk.LEFT)

        self.update()

    def write_slogan(self):
        print("Tkinter is easy to use!")

    def update(self):
        now = time.strftime("%H:%M:%S")
        self.et.set(now)
        self.frame.after(1000, self.update)



gpus[0].add_registers(root)



app = App(root)

app.et.set('test')
root.mainloop()

#tk.mainloop()

#ret = gpus[0].send_smc_msg(gpus[0].PPSMC_StopFanControl, curAdapter)
#ret = send_smc_msg(PPSMC_StartFanControl, curAdapter)




def print_pack(t_struct):
    for field in t_struct._fields_:
        print(field[0], getattr(t_struct, field[0]))


#print_pack(gpus[0].test.bits)


sys.exit()

def print_pack(t_struct):
    for field in t_struct._fields_:
        print(field[0], getattr(t_struct, field[0]))



pack_d = {}

regs = [['FDO_STATIC_DUTY', 'ixCG_FDO_CTRL0', 'rw']]

for t_prop, t_reg, t_rw in regs:
    if 'ix' in t_reg:
        if t_reg not in pack_d:
            pack_d[t_reg] = getattr(smu, t_reg + '_Pack')()
            pack_d[t_reg].binary_data = read_smc_ind_reg(getattr(smu, t_reg), curAdapter)
            print_pack(pack_d[t_reg].bits)
            print(t_prop, getattr(pack_d[t_reg].bits, t_prop))





sys.exit()



import smu_7_1_3 as smu
import polaris10_ppsmc as ppsmc

def malloc(iSize):
    return ctypes.addressof(ctypes.create_string_buffer(iSize))

def malloc_mem(iSize):
    return ctypes.create_string_buffer(iSize)


iomap = ctypes.cdll.LoadLibrary("Exeio.dll")


#VGAROMMappingForULPS
#Get_VGA_Bios_Infor
#Get_VGA_ChipInfor
#Read_VGA_Reg_Value
#Write_VGA_Reg_Value

ret = iomap.VGAROMMappingForULPS()
print(ret)


VGABiosInfo = malloc_mem(0x4000)
VGAChipInfo = malloc_mem(0x328)

ret = iomap.Get_VGA_Bios_Infor(ctypes.byref(VGABiosInfo))
#for i in range(len(VGABiosInfo)):
for i in range(512):
    print(VGABiosInfo[i].decode("ascii"), end='')
print(' ')


ret = iomap.Get_VGA_ChipInfor(ctypes.byref(VGAChipInfo))

for i in range(len(VGAChipInfo)):
    print(VGAChipInfo[i].hex(), end='')
print(' ')

iNumAdapters = int.from_bytes(VGAChipInfo[4], byteorder='little')
print('Detected %d adapter(s).' % iNumAdapters)
curAdapter = 0
pci_vendor_id = int.from_bytes(VGAChipInfo[0x2D8 + 4*curAdapter:0x2D8 + 4*curAdapter + 2], byteorder='little')
pci_device_id = int.from_bytes(VGAChipInfo[0x60 + 32*curAdapter:0x60 + 32*curAdapter + 2], byteorder='little')
pci_subvendor_id = int.from_bytes(VGAChipInfo[0x68 + 32*curAdapter:0x68 + 32*curAdapter + 2], byteorder='little')
pci_subdevice_id = int.from_bytes(VGAChipInfo[0x64 + 32*curAdapter:0x64 + 32*curAdapter + 2], byteorder='little')
print('%04X:%04X - %04X:%04X' % (pci_vendor_id, pci_device_id, pci_subvendor_id, pci_subdevice_id))



tempMem = malloc_mem(0x4)
ret = iomap.Read_VGA_Reg_Value(0x2A00, ctypes.byref(tempMem), 0)
print('%08X' % ret)
print(repr(tempMem.raw))

# read/write GPU register
def read_reg(t_reg, t_adapter):
    # actual address is register * 4
    ret = iomap.Read_VGA_Reg_Value(t_reg * 4, ctypes.byref(tempMem), t_adapter)
    print('read register [0x%08X] -> 0x%08X' % (t_reg, ret))
    return ret

def write_reg(t_reg, t_data, t_adapter):
    # actual address is register * 4
    ret = iomap.Write_VGA_Reg_Value(t_reg * 4, t_data, ctypes.byref(tempMem), t_adapter)
    print('write register [0x%08X] <= 0x%08X -> 0x%08X' % (t_reg, t_data, ret))
    return ret


# send messages to the GPU SMC
def send_smc_msg(t_reg, t_adapter):
    write_reg(smu.mmSMC_MESSAGE_1, t_reg, t_adapter)
    ret = read_reg(smu.mmSMC_MSG_ARG_1, t_adapter)
    return ret

def send_smc_msg_with_parameter(t_reg, t_data, t_adapter):
    write_reg(smu.mmSMC_MSG_ARG_1, t_data, t_adapter)
    write_reg(smu.mmSMC_MESSAGE_1, t_reg, t_adapter)
    ret = read_reg(smu.mmSMC_MSG_ARG_1, t_adapter)
    return ret

# read/write indirect registers through the SMC
def read_smc_ind_reg(t_ind_reg, t_adapter):
    write_reg(smu.mmSMC_IND_INDEX_1, t_ind_reg, t_adapter)
    ret = read_reg(smu.mmSMC_IND_DATA_1, t_adapter)
    return ret

def write_smc_ind_reg(t_ind_reg, t_data, t_adapter):
    write_reg(smu.mmSMC_IND_INDEX_1, t_ind_reg, t_adapter)
    ret = write_reg(smu.mmSMC_IND_DATA_1, t_data, t_adapter)
    return ret






def print_pack(t_struct):
    for field in t_struct._fields_:
        print(field[0], getattr(t_struct, field[0]))

if 0:
    #write_reg(mmSMC_MSG_ARG_1, 0x01, curAdapter)
    #write_reg(mmSMC_MESSAGE_1, PPSMC_MSG_SetVidOffset_1, curAdapter)
    #read_reg(mmSMC_MSG_ARG_1, curAdapter)
    ret = send_smc_msg_with_parameter(PPSMC_MSG_SetVidOffset_1, 0x00, curAdapter)
    print('0x%08x' % ret)
    #write_reg(mmSMC_MESSAGE_1, PPSMC_MSG_GetVidOffset_1, curAdapter)
    #read_reg(mmSMC_MSG_ARG_1, curAdapter)
    ret = send_smc_msg(PPSMC_MSG_GetVidOffset_1, curAdapter)
    print('0x%08x' % ret)


    ret = read_smc_ind_reg(ixCG_THERMAL_STATUS, curAdapter)
    print('0x%08x' % ret)

    ret = read_smc_ind_reg(ixCG_TACH_STATUS, curAdapter)
    print('0x%08x' % ret)


    #ret = write_smc_ind_reg(CG_FDO_CTRL1, 0x40092587, curAdapter)
    #print('0x%08x' % ret)

    ret = read_smc_ind_reg(ixCG_FDO_CTRL1, curAdapter)
    print('0x%08x' % ret)

    pack = ixCG_FDO_CTRL1_Pack()
    #pack.binary_data = struct.unpack("<i", ret)
    pack.binary_data = ret
    print_pack(pack.bits)
    pack.bits.FMIN_DUTY = 0
    print_pack(pack.bits)
    print('0x%08x' % pack.binary_data)

    #ret = write_smc_ind_reg(ixCG_FDO_CTRL1, pack.binary_data, curAdapter)
    #print('0x%08x' % ret)


    #ret = send_smc_msg(PPSMC_StopFanControl, curAdapter)
    ret = send_smc_msg(PPSMC_StartFanControl, curAdapter)

    pack_d = {}
    pack_d['ixCG_FDO_CTRL0'] = ixCG_FDO_CTRL0_Pack()
    pack_d['ixCG_FDO_CTRL1'] = ixCG_FDO_CTRL1_Pack()
    pack_d['ixCG_FDO_CTRL2'] = ixCG_FDO_CTRL2_Pack()

    pack_d['ixCG_FDO_CTRL0'].binary_data = read_smc_ind_reg(ixCG_FDO_CTRL0, curAdapter)
    pack_d['ixCG_FDO_CTRL1'].binary_data = read_smc_ind_reg(ixCG_FDO_CTRL1, curAdapter)
    pack_d['ixCG_FDO_CTRL2'].binary_data = read_smc_ind_reg(ixCG_FDO_CTRL2, curAdapter)

    print_pack(pack_d['ixCG_FDO_CTRL0'].bits)
    print_pack(pack_d['ixCG_FDO_CTRL1'].bits)
    print_pack(pack_d['ixCG_FDO_CTRL2'].bits)


    #pack_d['ixCG_FDO_CTRL0'].bits.FDO_STATIC_DUTY = pack_d['ixCG_FDO_CTRL1'].bits.FMAX_DUTY100
    pack_d['ixCG_FDO_CTRL0'].bits.FDO_STATIC_DUTY = 10
    write_smc_ind_reg(ixCG_FDO_CTRL0, pack_d['ixCG_FDO_CTRL0'].binary_data, curAdapter)
    write_smc_ind_reg(ixCG_FDO_CTRL2, pack_d['ixCG_FDO_CTRL2'].binary_data, curAdapter)


pack_d = {}

regs = [['FDO_STATIC_DUTY', 'ixCG_FDO_CTRL0', 'rw']]

for t_prop, t_reg, t_rw in regs:
    if 'ix' in t_reg:
        if t_reg not in pack_d:
            pack_d[t_reg] = getattr(smu, t_reg + '_Pack')()
            pack_d[t_reg].binary_data = read_smc_ind_reg(getattr(smu, t_reg), curAdapter)
            print_pack(pack_d[t_reg].bits)
            print(t_prop, getattr(pack_d[t_reg].bits, t_prop))
