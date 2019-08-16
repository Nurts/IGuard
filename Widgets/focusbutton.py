import tkinter as tk
class FocusButton(tk.Button):
    def on_enter(self, event):
        self.configure(bg = self.in_color)
    
    def on_leave(self, event):
        self.configure(bg = self.out_color)

    def __init__(self, parent, in_color, out_color, **kwargs):
        self.in_color = in_color
        self.out_color = out_color
        tk.Button.__init__(self, parent, bg = out_color, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)