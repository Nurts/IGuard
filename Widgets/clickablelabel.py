import tkinter as tk
class ClickableLabel(tk.Label):
    def on_enter(self, e):
        if not self.disabled:
            self.configure(bg = self.in_color)


    def on_leave(self, e):
        if not self.disabled:
            self.configure(bg = self.out_color)
    
    def __init__(self, parent, in_color, out_color, clicked_color, **kwargs):
        self.in_color = in_color
        self.out_color = out_color
        self.clicked_color = clicked_color
        self.disabled = False

        tk.Label.__init__(self, parent, bg = self.out_color, fg = self.clicked_color, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def click(self):
        if not self.disabled:
            self.configure(bg = self.clicked_color, fg = self.out_color)
            self.disabled = True
        else:
            self.configure(bg = self.out_color, fg = self.clicked_color)
            self.disabled = False
