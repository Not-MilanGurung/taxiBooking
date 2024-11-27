from tkinter import Misc
from tkinter.ttk import Style

const_bg = '#9C98F6'
const_main_bg = '#0D1119'
const_secondary = '#1E202D'
const_font_colour = '#E8FCBF'
const_accent = '#F29DA2'

class TaxiAppStyle(Style):

    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)
        self.framStyle()
        self.buttonStyle()
        self.labelStyle()
        self.entryStyle()
        self.fontStyle()

    def fontStyle(self):
        self.configure('.', font=('Helvetica', 12) )

    def framStyle(self):
        self.configure('TFrame', background = const_bg)
        self.configure('SideBar.TFrame', background = const_main_bg)
        self.configure('LoginRegister.TFrame', background= const_main_bg)
        self.configure('MainBar.TFrame', background= const_secondary)
        self.configure('Username_Frame.TFrame', background=const_secondary)

    def buttonStyle(self):
        self.configure('TButton', background= const_secondary, foreground=const_font_colour)
        self.map('TButton', background=[('active', const_accent)])

    def entryStyle(self):
        self.configure('user.TEntry', fieldbackground = const_main_bg, foreground = const_font_colour )

    def labelStyle(self):
        self.configure('TLabel', background=const_secondary,foreground= const_font_colour)
        self.configure('loginTitleLabel.TLabel', background=const_main_bg,foreground= const_font_colour, font=('Helvetica', 24))
        self.configure('mainBgText.TLabel', background=const_main_bg,foreground= const_font_colour)

