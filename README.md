# VRMtool
In progress version of VRMtool version 2.
Version 1 can be found here:
http://www.overclock.net/t/1605757/vrmtool-a-simple-tool-to-read-and-write-to-i2c-vrm-controllers

VRMtool allows access to low level registers of AMD GPUs and their VRM controllers. GPU register access is implemented through direct MMIO. I2C and PMBus access to VRM controllers is implemented through the AMD ADL interface.

DISCLAIMER: I take no responsibility at all. I can not be held responsible. Everything you do is on your own risk. Fiddling with GPU and VRM registers is potentially harmfull to your computer hardware.

# Requirements
Currently limited to AMD Radeon RX 480 reference cards on windows.


# Example usage
```
python vrmtool.py
```


# TODO
* finish up IR3567B I2C registers and parsing
* PMBus interface and parsing
* graph plotting of VRM read out values
* find out memory ECC register
* add AMD ADL official overclocking support
* linux and maybe Mac support
* direct I2C access through GPU MMIO
