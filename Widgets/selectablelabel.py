import tkinter as tk

class SelectableLabel(tk.Text):

    def __init__(self, parent, text,**kwargs):
        tk.Text.__init__(self, parent, **kwargs)
        self.insert(1.0, text)
        self.configure(state = "disabled", inactiveselectbackground = self.cget("selectbackground"), bg = parent.cget('bg'), relief=tk.FLAT)
