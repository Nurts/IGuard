import tkinter as tk
import requests
import json
from Widgets import PlaceholderEntry, PasswordEntry, FocusButton, SelectableLabel, VerticalScrolledFrame
from tkinter import messagebox
import Errors

class UsersList(tk.Frame):

    def __init__(self, parent, list_of_users, list_of_ids, session, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        
        self.session = session
        self.list_of_ids = list_of_ids
        self.list_of_users = list_of_users
        self.addRegFrame()

        self.addUserList()

    def addUserList(self):
        
        try:
            url = "https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/users"
            response = self.session.get(url = url)
        except:
            Errors.networkConnectionError()
            return
        
        self.user_list = VerticalScrolledFrame(self, bg = 'white')
        self.user_list.interior.configure(bg = 'white')
        self.user_list.pack(side = tk.BOTTOM, fill = 'both', expand = True)
        self.user_frames = []
        self.users = response.json()
        
        
        for user in self.users:
            self.addUser(user)
    
    def addUser(self, user):
        user_frame = tk.Frame(self.user_list.interior, bg = '#3A79D1')

        self.list_of_users.append(user['login'])
        self.list_of_ids.append(user['id'])

        login_label = tk.Label(user_frame, text = "login: {}".format(user['login']), font = 'Sans 11', height = 2, bg = '#3A79D1', fg = 'white')
        login_label.pack(side = tk.LEFT, fill = tk.Y, expand = True)

        name_label = tk.Label(user_frame, text = "Full Name: {} {}".format(user['name'], user['surname']), font = 'Sans 11', height = 2, bg = '#3A79D1', fg = 'white')
        name_label.pack(side = tk.LEFT, fill = tk.Y, expand = True)

        email_label = tk.Label(user_frame, text = "email: {}".format(user['email']), font = 'Sans 11', height = 2, bg = '#3A79D1', fg = 'white')
        email_label.pack(side = tk.LEFT, fill = tk.Y, expand = True)

        delete_btn = FocusButton(user_frame, text = 'Delete', in_color = '#f05454', out_color = '#c90404', fg = 'white', relief = tk.FLAT)
        delete_btn.configure(command = lambda id = user['id'], login = user['login'] : self.deleteUser(id, login))
        delete_btn.pack(side = tk.RIGHT, fill = tk.Y, expand = False, pady = 10, padx = 10)

        user_frame.pack(side = tk.BOTTOM, fill = tk.X, expand = True, padx = 10, pady = 10)

        self.user_frames.append(user_frame)
    
    def findAndShowUser(self, username):
        for user_frame in self.user_frames:
            user_frame.pack_forget()
        
        
        for i in range(len(self.list_of_users)):
            if username in self.list_of_users[i]:
                self.user_frames[i].pack(side = tk.BOTTOM, fill = tk.X, expand = True, padx = 10, pady = 10)
    
    def deleteUser(self, id, login):

        if messagebox.askokcancel("Delete User", "Do you want to delete {}?".format(login), parent = self.user_list.interior):
            
            try:
                url = 'https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/user/{}'.format(id)
                res = self.session.delete(url = url)
                print(res.text)
            except:
                Errors.networkConnectionError()
                return
            
            for i, user in enumerate(self.list_of_users):
                if(user == login):
                    self.user_frames[i].destroy()
                    del self.user_frames[i]
                    del self.list_of_users[i]
                    del self.list_of_ids[i]
                    break



    def addRegFrame(self):
        
        self.reg_frame = tk.Frame(self, bg = '#3A79D1')
        
        self.username = PlaceholderEntry(self.reg_frame, placeholder = 'Username', relief = tk.RAISED)
        self.username.grid(row = 0, column = 0, sticky = 'nsew', padx = 10, pady = 5)

        self.email = PlaceholderEntry(self.reg_frame, placeholder = 'Email', relief = tk.RAISED)
        self.email.grid(row = 0, column = 1, columnspan = 2, sticky = 'nsew', padx = 10, pady = 5)

        self.first_name = PlaceholderEntry(self.reg_frame, placeholder = 'First Name', relief = tk.RAISED)
        self.first_name.grid(row = 1, column = 0, sticky = 'nsew', padx = 10, pady = 5)

        self.second_name = PlaceholderEntry(self.reg_frame, placeholder = 'Surname', relief = tk.RAISED)
        self.second_name.grid(row = 1, column = 1, columnspan = 2, sticky = 'nsew', padx = 10, pady = 5)

        self.city = PlaceholderEntry(self.reg_frame, placeholder = 'City', relief = tk.RAISED)
        self.city.grid(row = 2, column = 0, sticky = 'nsew', padx = 10, pady = 5)

        self.street = PlaceholderEntry(self.reg_frame, placeholder = 'Street', relief = tk.RAISED)
        self.street.grid(row = 2, column = 1, sticky = 'nsew', padx = 10, pady = 5)

        self.house = PlaceholderEntry(self.reg_frame, placeholder = 'House', relief = tk.RAISED)
        self.house.grid(row = 2, column = 2, sticky = 'nsew', padx = 10, pady = 5)

        self.password = PasswordEntry(self.reg_frame, placeholder = 'Password', relief = tk.RAISED)
        self.password.grid(row = 3, column = 0, sticky = 'nsew', padx = 10, pady = 5)

        self.password_confirmation = PasswordEntry(self.reg_frame, placeholder = 'Password Confirmation', width = 25, relief = tk.RAISED)
        self.password_confirmation.grid(row = 3, column = 1, sticky = 'nsew', padx = 10, pady = 5)

        self.add_btn = FocusButton(self.reg_frame, in_color = '#32bf1d', out_color = '#149600', text = 'Register User', fg = 'white', command = self.registerUser)
        self.add_btn.grid(row = 3, column = 2, sticky = 'nsew', padx = 10, pady = 5)

        self.reg_frame.pack(side = tk.TOP, fill = tk.X)
        
    def registerUser(self):
        params = {
            'login' : self.username.get_data(),
            'name' : self.first_name.get_data(),
            'surname' : self.second_name.get_data(),
            'email' : self.email.get_data(),
            'city' : self.city.get_data(),
            'street' : self.street.get_data(),
            'house' : self.house.get_data(),
            'password' : self.password.get_data(),
            'password_confirmation' : self.password_confirmation.get_data()
        }

        try:
            url = "https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/register/user"
            res = dict(self.session.post(url = url, data = params).json())
        except:
            Errors.networkConnectionError()
            return
        
        if "errors" in res.keys():
            
            error_text = ""
            for error in res["errors"]:
                error_text += error + "\n"
            
            errorLabel = tk.Label(self, bg = 'red', fg = 'white', text = error_text)
            errorLabel.pack(side = tk.TOP, fill = tk.X)
            errorLabel.bind("<Button-1>", lambda e : errorLabel.destroy())

        else:
            self.addUser(res)
