import tkinter as tk
import PIL.Image, PIL.ImageTk
from Widgets import PlaceholderEntry, PasswordEntry
from Guest import GuestApp
from Admin import AdminWindow
import Errors
import requests

window_config = {
    'window_title' : "IGuard Desktop",
    'bg_color' : '#3A79D1',
    'center_img' : './assets/authIcon.png',
    'loginbtn_text' : 'Login',
    'guestbtn_text' : 'Login as Guest',
    'password_text' : 'Password',
    'username_text' : 'Username',
    'font' : 'Arial 13'
}

auth_state = 0
admin_session = None

class AuthWindow(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("350x450+500+150")
        self.title(window_config['window_title'])
        self.resizable(False, True)
        self.configure(background = window_config['bg_color'])
        
        try:
            self.img = PIL.ImageTk.PhotoImage(PIL.Image.open(window_config['center_img']))

            self.img_label = tk.Label(self, image = self.img, borderwidth = 0, highlightthickness = 0)
            self.img_label.pack(side = tk.TOP)
        except:
            print("Coulnd't load image !")
            
        self.username_box = PlaceholderEntry(self, placeholder = window_config['username_text'], width = 30, font = window_config['font'])
        self.username_box.pack(side = tk.TOP, pady = 10)

        self.password_box = PasswordEntry(self, placeholder= window_config['password_text'], width = 30, font = window_config['font'])
        self.password_box.pack(side = tk.TOP, pady = 10)
        self.password_box.bind('<Return>', lambda e : self.loginCommand())

        self.login_btn = tk.Button(self, text = window_config['loginbtn_text'], width = 30, relief = tk.FLAT, command = self.loginCommand, bg = 'white')
        self.login_btn.pack(side = tk.TOP, pady = 3)
        
        self.guest_btn = tk.Button(self, text = window_config['guestbtn_text'], width = 30, relief = tk.FLAT, command = self.guestCommand, bg = 'white')
        self.guest_btn.pack(side = tk.TOP, pady = 10)


    def loginCommand(self):
        global admin_session
        params = {
            'username' : self.username_box.get_data(),
            'password' : self.password_box.get_data()
        }

        url = 'https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/login'
        admin_session = requests.Session()
        try:
            response = admin_session.post(url, data = params)
        except:
            Errors.networkConnectionError()
            return

        response = dict(response.json())
        if 'is_admin' not in response.keys():
            Errors.authorizationError()
        else:
            if response['is_admin'] is None:
                Errors.notAdminAuthorizationError()
            else:
                global auth_state
                auth_state = 1
                self.destroy()

    
    def guestCommand(self):
        global auth_state
        auth_state = 2
        self.destroy()
        

if __name__ == '__main__':
    should_start = [True]
    while(should_start[0]):
        should_start[0] = False
        admin_session = None
        auth = AuthWindow()
        auth.mainloop()

        if(auth_state == 1):
            app = AdminWindow(should_start, admin_session)
            app.mainloop()
        elif(auth_state == 2):
            app = GuestApp(should_start)
            app.mainloop()
        
        auth_state = 0




        