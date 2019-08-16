import tkinter as tk
from UsersList import UsersList
from CamerasFrame import CamerasFrame
from Widgets import ClickableLabel, FocusButton
from ttkwidgets.autocomplete import AutocompleteCombobox

class AdminWindow(tk.Tk):

    def __init__(self, restart_var, session):
        
        tk.Tk.__init__(self)
        self.restart_var = restart_var
        self.session = session
        self.window_config = {
            "title" : "IGuard Desktop Admin",
            "cam-nav-text" : "Cameras",
            "user-nav-text" : "Users",
            "filter-btn-text" : "Search",
            "filter-reset-btn-text" : "Show All",
            "filter-label" : 'Select User:'
        }
        self.geometry("700x600")
        self.title(self.window_config["title"])

        self.navbar = tk.Frame(self)
        self.navbar.pack(side = tk.TOP, fill = tk.X)

        self.camBtn = ClickableLabel(self.navbar, '#cfebff', 'white', '#3A79D1', text = self.window_config['cam-nav-text'], font = "Arial 15", height = 3)
        self.camBtn.bind("<Button-1>", lambda e : self.showCameras())
        self.camBtn.pack(side = tk.LEFT, fill = 'both', expand = True)
        
        self.usersBtn = ClickableLabel(self.navbar, '#cfebff', 'white', '#3A79D1', text = self.window_config['user-nav-text'], font = "Arial 15", height = 3)
        self.usersBtn.bind("<Button-1>", lambda e : self.showUsers())
        self.usersBtn.pack(side = tk.RIGHT, fill = 'both', expand = True)
        
        self.camBtn.click()

        self.protocol("WM_DELETE_WINDOW", self.logOut)

        self.cam_frame = CamerasFrame(self)
        self.cam_frame.pack(side = tk.TOP, fill = 'both', expand = True)

        self.users_frame = UsersList(self, bg = '#3A79D1', list_of_users = self.cam_frame.list_of_users, list_of_ids = self.cam_frame.list_of_ids, session = self.session)

        self.filter_frame = tk.Frame(self, bg = 'white')
        self.filter_frame.pack(side = tk.BOTTOM, fill = tk.X)
        
        tk.Label(self.filter_frame, text = self.window_config['filter-label'], bg = 'white', font = 'Arial 11').pack(side = tk.LEFT, fill = tk.Y, pady = 10)

        self.filter_user_combobox = AutocompleteCombobox(self.filter_frame, completevalues = self.cam_frame.list_of_users)
        self.filter_user_combobox.pack(side = tk.LEFT, fill = tk.Y, pady = 10, padx = 10)

        self.filter_button = FocusButton(self.filter_frame, in_color = '#325080', out_color = '#3A79D1', text = self.window_config['filter-btn-text'], command = self.filterByUser, fg = 'white', relief = tk.FLAT)
        self.filter_button.pack(side = tk.LEFT, fill = tk.Y, pady = 10, padx = 10)

        self.filter_reset_button = FocusButton(self.filter_frame, in_color = '#325080', out_color = '#3A79D1', text = self.window_config['filter-reset-btn-text'], command = self.resetFilter, fg = 'white', relief = tk.FLAT)
        self.filter_reset_button.pack(side = tk.LEFT, fill = tk.Y, pady = 10, padx = 10)

    def resetFilter(self):
        if(self.usersBtn.disabled):
            self.users_frame.findAndShowUser("")
        else:
            self.cam_frame.findByUser(None, True)

    def filterByUser(self):
        username = self.filter_user_combobox.get()
        print(username)
        if(self.usersBtn.disabled):
            self.users_frame.findAndShowUser(username)
        else:
            self.cam_frame.findByUser(username)

    def showCameras(self):
        if(self.camBtn.disabled):
            return
        self.camBtn.click()
        self.usersBtn.click()
        self.users_frame.pack_forget()
        self.cam_frame.pack(side = tk.TOP, fill = 'both', expand = True)

    def showUsers(self):
        if(self.usersBtn.disabled):
            return
        self.usersBtn.click()
        self.camBtn.click()
        self.cam_frame.pack_forget()
        self.users_frame.pack(side = tk.TOP, fill = 'both', expand = True)

    def logOut(self):
        self.restart_var[0] = True
        del self.session
        self.destroy()