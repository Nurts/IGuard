import tkinter as tk

class PasswordEntry(tk.Entry):
    def foc_in(self, event):
        if self.get() == self.placeholder :
            self.configure(show = '*', fg = 'black')
            self.delete(0, tk.END)

    def foc_out(self, event):
        if self.get() == '':
            self.configure(show = '', fg = 'gray25')
            self.insert(0, self.placeholder)

    def __init__(self, parent, placeholder, **kwargs):

        tk.Entry.__init__(self, parent, kwargs, fg = 'gray25')

        self.placeholder = placeholder

        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.foc_in)
        self.bind('<FocusOut>', self.foc_out)
    
    def get_data(self):
        data = tk.Entry.get(self)
        if(data == self.placeholder):
            return ''
        else:
            return data