
import tkinter as tk

class fidget():
    def __init__():
        #self.props['FAN | Static fan speed'] = ['value', 'int', 'rw', 'FDO_STATIC_DUTY', 'ixCG_FDO_CTRL0']

        self.label = 'lore ipsum'
        self.tk_label = None

        self.tk_entry_text = tk.StringVar()
        self.tk_entry = None

        self.button = 'press me'
        self.tk_button = None

        self.permission = 'rw'

    def set(self, t_par):
        self.tk_entry_text.set(t_par)

    def get(self):
        return self.tk_entry_text.get()
