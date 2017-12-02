
import tkinter as tk



REG_Loop1_VID = 0x93
REG_Loop1_Temp = 0x9E





class FidgetVRMRegister():
    def __init__(self, vrminst, root, reg):
        self.vrminst = vrminst
        self.root = root
        self.reg = reg

        self.row = tk.Frame(self.root)
        self.row.pack(side=tk.TOP, anchor=tk.W)

        self.lab = tk.Label(self.row, text=self.reg, width=22)
        self.lab.pack(side=tk.LEFT)

        self.bt_get = tk.Button(self.row, text="Get", command=self.get_reg)
        self.bt_get.pack(side=tk.LEFT)

        #self.bt_set = tk.Button(self.row, text="Set", command=self.set_reg)
        #self.bt_set.pack(side=tk.LEFT)

        self.data = -1

        self.data_variable = tk.StringVar()
        self.data_entry = tk.Entry(self.row, textvariable=self.data_variable, justify=tk.CENTER, width=7)
        self.data_variable.set(self.data)
        self.data_entry.pack(side=tk.LEFT)



    def get_reg(self):
        print('get', self.reg)
        self.data = self.vrminst.read_register(self.reg)
        self.data_variable.set(self.data)

    def set_reg(self):
        print('set', self.reg)
        t_struct = self.data.bits
        for field in t_struct._fields_:
            print(field[0], self.entries[field[0]].get())
            setattr(t_struct, field[0], int(self.entries[field[0]].get()))
        self.set_reg_hw(self.data.binary_data)
        self.get_reg()




class ir3567b():
    def __init__(self, adl, adapterid, line, address):
        self.adl = adl
        self.adapterid = adapterid
        self.line = line
        self.address = address


    def read_register(self, t_reg):
        return self.adl.I2C_read_byte(self.line, self.address, globals()[t_reg], self.adapterid)


    def add_registers(self, root):
        vrm_registers = ['REG_Loop1_VID', 'REG_Loop1_Temp']
        for reg in vrm_registers:
            FidgetVRMRegister(self, root, reg)
