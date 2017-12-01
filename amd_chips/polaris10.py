import ctypes
import struct
import os

import tkinter as tk

from amd_ips import polaris10_ppsmc as ppsmc
from amd_ips import smu_7_1_3 as smu
from amd_ips import gfx80 as gfx
from amd_ips import gmc81 as gmc




class FidgetBase():
    def __init__(self, gpuinst, root, reg_type, reg):
        pass

class FidgetMsgs(FidgetBase):
    def __init__(self, gpuinst, root, msg_l):
        self.gpuinst = gpuinst
        self.root = root
        self.msg_l = msg_l

        self.row = tk.Frame(self.root)
        self.row.pack(side=tk.TOP, anchor=tk.W)

        for msg in msg_l:
            # use lambda function to pass paramter to tkinter callback
            bt = tk.Button(self.row, text=msg, command=lambda: self.send_msg(msg))
            bt.pack(side=tk.LEFT)

    def send_msg(self, msg):
        print('send', msg)
        self.gpuinst.send_smc_msg(getattr(ppsmc, msg))



class FidgetRegister(FidgetBase):
    def __init__(self, gpuinst, root, reg_type, reg):
        self.gpuinst = gpuinst
        self.root = root
        self.reg_type = reg_type
        self.reg = reg

        self.row = tk.Frame(self.root)
        self.row.pack(side=tk.TOP, anchor=tk.W)

        self.lab = tk.Label(self.row, text=self.reg, width=22)
        self.lab.pack(side=tk.LEFT)

        self.bt_get = tk.Button(self.row, text="Get", command=self.get_reg)
        self.bt_get.pack(side=tk.LEFT)

        self.bt_set = tk.Button(self.row, text="Set", command=self.set_reg)
        self.bt_set.pack(side=tk.LEFT)

        self.data = getattr(self.reg_type, self.reg + '_Pack')()

        self.entries = {}

        t_struct = self.data.bits
        for field in t_struct._fields_:
            #print(field[0], getattr(t_struct, field[0]))

            lab2 = tk.Label(self.row, text=field[0])
            lab2.pack(side=tk.LEFT, padx=(5,0))

            et = tk.StringVar()
            entry = tk.Entry(self.row, textvariable = et, justify=tk.CENTER, width=7)
            et.set(0)
            entry.pack(side=tk.LEFT)
            self.entries[field[0]] = et



    def get_reg(self):
        print('get', self.reg)
        self.data.binary_data = self.get_reg_hw()
        t_struct = self.data.bits
        for field in t_struct._fields_:
            self.entries[field[0]].set(getattr(t_struct, field[0]))

    def set_reg(self):
        print('set', self.reg)
        t_struct = self.data.bits
        for field in t_struct._fields_:
            print(field[0], self.entries[field[0]].get())
            setattr(t_struct, field[0], int(self.entries[field[0]].get()))
        self.set_reg_hw(self.data.binary_data)
        self.get_reg()


    def get_reg_hw(self):
        return self.gpuinst.read_reg(getattr(self.reg_type, self.reg))

    def set_reg_hw(self, binary_data):
        self.gpuinst.write_reg(getattr(self.reg_type, self.reg), binary_data)


class FidgetIndirectSMCRegister(FidgetRegister):
    def __init__(self, gpuinst, root, reg_type, reg):
        super().__init__(gpuinst, root, reg_type, reg)


    def get_reg_hw(self):
        return self.gpuinst.read_smc_ind_reg(getattr(self.reg_type, self.reg))

    def set_reg_hw(self, binary_data):
        self.gpuinst.write_smc_ind_reg(getattr(self.reg_type, self.reg), binary_data)




class polaris10():
    def __init__(self, exeio, adapterid):
        self.exeio = exeio
        self.adapterid = adapterid


    def add_registers(self, root):
        gmc_registers = ['mmMC_SEQ_RAS_TIMING', 'mmMC_SEQ_CAS_TIMING', 'mmMC_SEQ_MISC_TIMING', 'mmMC_SEQ_MISC_TIMING2', 'mmMC_ARB_DRAM_TIMING', 'mmMC_ARB_DRAM_TIMING2']
        for reg in gmc_registers:
            FidgetRegister(self, root, gmc, reg)

        smu_registers = ['ixCG_THERMAL_STATUS', 'ixCG_TACH_STATUS', 'ixCG_FDO_CTRL0', 'ixCG_FDO_CTRL1', 'ixCG_FDO_CTRL2']
        for reg in smu_registers:
            FidgetIndirectSMCRegister(self, root, smu, reg)


        FidgetMsgs(self, root, ['PPSMC_StartFanControl', 'PPSMC_StopFanControl'])

        #FidgetRegister(self, root, gfx, 'mmSQC_EDC_CNT')


    # read write GPU register
    def read_reg(self, t_reg):
        ret = self.exeio.read_reg(t_reg, self.adapterid)
        return ret

    def write_reg(self, t_reg, t_data):
        ret = self.exeio.write_reg(t_reg, t_data, self.adapterid)
        return ret


    # send messages to the GPU SMC
    def send_smc_msg(self, t_reg):
        self.exeio.write_reg(smu.mmSMC_MESSAGE_1, t_reg, self.adapterid)
        ret = self.exeio.read_reg(smu.mmSMC_MSG_ARG_1, self.adapterid)
        return ret

    def send_smc_msg_with_parameter(self, t_reg, t_data):
        self.exeio.write_reg(smu.mmSMC_MSG_ARG_1, t_data, self.adapterid)
        self.exeio.write_reg(smu.mmSMC_MESSAGE_1, t_reg, self.adapterid)
        ret = self.exeio.read_reg(smu.mmSMC_MSG_ARG_1, self.adapterid)
        return ret

    # read/write indirect registers through the SMC
    def read_smc_ind_reg(self, t_ind_reg):
        self.exeio.write_reg(smu.mmSMC_IND_INDEX_1, t_ind_reg, self.adapterid)
        ret = self.exeio.read_reg(smu.mmSMC_IND_DATA_1, self.adapterid)
        return ret

    def write_smc_ind_reg(self, t_ind_reg, t_data):
        self.exeio.write_reg(smu.mmSMC_IND_INDEX_1, t_ind_reg, self.adapterid)
        ret = self.exeio.write_reg(smu.mmSMC_IND_DATA_1, t_data, self.adapterid)
        return ret
