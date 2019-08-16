import tkinter as tk

class BlinkingLabel(tk.Label):

    def __init__(self, parent, first_color, second_color, period = 500, **kwargs):
        tk.Label.__init__(self, parent, bg = first_color, **kwargs)

        self.period = 500
        self.first_color = first_color
        self.second_color = second_color
        self.on = True
        self.after(self.period, self.blink)
    
    def blink(self):
        if(self.on):
            self.configure(bg = self.second_color)
        else:
            self.configure(bg = self.first_color)
        self.on = not self.on
        self.after(self.period, self.blink)