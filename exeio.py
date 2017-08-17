import ctypes
import struct
import os


def malloc(iSize):
    return ctypes.addressof(ctypes.create_string_buffer(iSize))

def malloc_mem(iSize):
    return ctypes.create_string_buffer(iSize)





#VGAROMMappingForULPS
#Get_VGA_Bios_Infor
#Get_VGA_ChipInfor
#Read_VGA_Reg_Value
#Write_VGA_Reg_Value


class exeio():
    def __init__(self):
        self.iomap = ctypes.cdll.LoadLibrary("Exeio.dll")

        ret = self.iomap.VGAROMMappingForULPS()
        print(ret)


        self.VGABiosInfo = malloc_mem(0x4000)
        self.VGAChipInfo = malloc_mem(0x328)
        self.tempMem = malloc_mem(0x4)

        ret = self.iomap.Get_VGA_Bios_Infor(ctypes.byref(self.VGABiosInfo))
        #for i in range(len(VGABiosInfo)):
        for i in range(512):
            print(self.VGABiosInfo[i].decode("ascii"), end='')
        print(' ')


        ret = self.iomap.Get_VGA_ChipInfor(ctypes.byref(self.VGAChipInfo))

        for i in range(len(self.VGAChipInfo)):
            print(self.VGAChipInfo[i].hex(), end='')
        print(' ')

        self.iNumAdapters = int.from_bytes(self.VGAChipInfo[4], byteorder='little')
        print('Detected %d adapter(s):' % self.iNumAdapters)
        for curAdapter in range(self.iNumAdapters):
            pci_vendor_id = int.from_bytes(self.VGAChipInfo[0x2D8 + 4*curAdapter:0x2D8 + 4*curAdapter + 2], byteorder='little')
            pci_device_id = int.from_bytes(self.VGAChipInfo[0x60 + 32*curAdapter:0x60 + 32*curAdapter + 2], byteorder='little')
            pci_subvendor_id = int.from_bytes(self.VGAChipInfo[0x68 + 32*curAdapter:0x68 + 32*curAdapter + 2], byteorder='little')
            pci_subdevice_id = int.from_bytes(self.VGAChipInfo[0x64 + 32*curAdapter:0x64 + 32*curAdapter + 2], byteorder='little')
            print('   %d: %04X:%04X - %04X:%04X' % (curAdapter, pci_vendor_id, pci_device_id, pci_subvendor_id, pci_subdevice_id))



        #ret = self.iomap.Read_VGA_Reg_Value(0x2A00, ctypes.byref(tempMem), 0)
        #print('%08X' % ret)
        #print(repr(tempMem.raw))

    # read/write GPU register
    def read_reg(self, t_reg, t_adapter):
        # actual address is register * 4
        ret = self.iomap.Read_VGA_Reg_Value(t_reg * 4, ctypes.byref(self.tempMem), t_adapter) & 0xffffffff
        print('read register [0x%08X] -> 0x%08X' % (t_reg, ret))
        return ret

    def write_reg(self, t_reg, t_data, t_adapter):
        # actual address is register * 4
        print('write register [0x%X] <= 0x%X' % (t_reg, t_data))
        ret = self.iomap.Write_VGA_Reg_Value(t_reg * 4, t_data & 0xffffffff, ctypes.byref(self.tempMem), t_adapter)
        print('write register [0x%08X] <= 0x%08X -> 0x%08X' % (t_reg, t_data, ret))
        return ret





#def print_pack(t_struct):
#    for field in t_struct._fields_:
#        print(field[0], getattr(t_struct, field[0]))
