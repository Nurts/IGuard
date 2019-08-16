import tkinter as tk


def networkConnectionError():
    tk.messagebox.showerror("Error", "Couldn't connect to database. Please check your internet connection !")

def authorizationError():
    tk.messagebox.showerror("Error", "Invalid username or password. Please try again!")

def notAdminAuthorizationError():
    tk.messagebox.showerror("Error", "Only Administartors are allowed to log in to desktop application!")

def configNotFoundError():
    tk.messagebox.showerror("Error", "Configuration of system is not found! Please contact the developers!")

def unknownError():
    tk.messagebox.showerror("Error", "Operation is failed! Something went wrong. Please contact the developers")

def invalidVideoAdress():
    tk.messagebox.showerror("Invalid Adress", "Invalid video source!, Please type again")