import ctypes
import struct
import os
import sys
import time

import tkinter as tk

from amd_tools import exeio
from amd_tools import amdadl

from amd_chips import polaris10

from vrms import ir3567b


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



# initialize AMD ADL interface
adl = amdadl.amdadl()

# reference RX 480 has an IR3567B VRM controller
# with I2C at line 04 and address 08
# and PMBUS at line 04 and address 70
# TODO: auto-detection of I2C/PMBUS devices
vrms = []
vrms.append(ir3567b.ir3567b(adl, 0, 0x04, 0x08))

vrms[0].add_registers(root)

#adl.I2C_read_byte(0x04, 0x08, 0x0D, adl.active_ids[0])


# run tkinter UI
app = App(root)
root.title('VRMtool')
root.mainloop()






def print_pack(t_struct):
    for field in t_struct._fields_:
        print(field[0], getattr(t_struct, field[0]))


#print_pack(gpus[0].test.bits)
