import ctypes
import struct
import os
import sys
import time

import tkinter as tk

from amd_tools import exeio
from amd_chips import polaris10


# fix bad font rendering on screens with high dpi scaling activated
ctypes.windll.shcore.SetProcessDpiAwareness(1)


root = tk.Tk()

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

        self.update()

    def update(self):
        now = time.strftime("%H:%M:%S")
        self.et.set(now)
        self.frame.after(1000, self.update)


# uses memory mapped I/O to get direct access to GPU registers and memory
iomap = exeio.exeio()

# assume first gpu is Polaris 10 based
# TODO: implement auto-detection
gpus = []
gpus.append(polaris10.polaris10(iomap, 0))

# add buttons/labels for direct GPU manipulation to UI
gpus[0].add_registers(root)


# run tkinter UI
app = App(root)
root.title('VRMtool')
root.mainloop()






def print_pack(t_struct):
    for field in t_struct._fields_:
        print(field[0], getattr(t_struct, field[0]))


#print_pack(gpus[0].test.bits)


sys.exit()





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
