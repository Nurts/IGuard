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

class PlaceholderEntry(tk.Entry):
    def foc_in(self, event):
        if self.get() == self.placeholder :
            self.configure(fg = 'black')
            self.delete(0, tk.END)

    def foc_out(self, event):
        if self.get() == '':
            self.configure(fg = 'gray25')
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

    def clear(self):
        self.delete(0, tk.END)
        self.configure(fg = 'gray25')
        self.insert(0, self.placeholder)