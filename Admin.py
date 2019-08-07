import tkinter as tk
from tkinter import messagebox
from VerticalScrolledFrame import VerticalScrolledFrame
from UsersList import UsersList
from VideoCap import Video
from LineConfig import PaintApp
from Widgets import ClickableLabel, FocusButton, PlaceholderEntry
from Combobox import Combobox_Autocomplete
import json
import random

class AdminWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)


        self.window_config = {
            "title" : "IGuard Desktop Admin",
            "cam-nav-text" : "Cameras",
            "user-nav-text" : "Users"
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

        self.cam_frame = CamerasFrame(self)
        self.cam_frame.pack(side = tk.TOP, fill = 'both', expand = True)


        self.users_frame = UsersList(self, bg = '#3A79D1')

        # self.main_frame =  ScrollFrame(self.window, relief = tk.FLAT, width = 500, height = 500)
        # self.main_frame.pack(fill = tk.BOTH, expand = True)
        # #self.main_frame.viewPort.pack(fill = tk.BOTH)
        # self.videos = videos
        # self.vid_frames = []
        # for i, video in enumerate(videos):
        #     self.addLabel(video.video_source, i)

        
        # self.add_frame = tk.Frame(self.main_frame.viewPort, borderwidth = 5)
        # self.add_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10, expand = False)
        # add_label = tk.Label(self.add_frame, text = "Video Path: ")
        # self.add_entry = tk.Entry(self.add_frame, width = 40)
        # add_button = tk.Button(self.add_frame, text = "Add Video", command = self.addVideo)
        
        # add_button.pack(side = tk.RIGHT)
        # add_label.pack(side = tk.LEFT)
        # self.add_entry.pack(side = tk.LEFT)

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


class CamerasFrame(tk.Frame):

    def __init__(self, parent, bg = '#3A79D1',  **kwargs):
        tk.Frame.__init__(self, parent, bg = bg, **kwargs)

        self.scrollable = VerticalScrolledFrame(self, bg = bg, **kwargs)
        self.scrollable.interior.configure(bg = bg)
        self.scrollable.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        self.vid_list = []

        self.addVidForm()

        with open('config.json') as f:
            config = json.load(f)
            self.video_sources = config['video_sources']
            self.points_sources = config['points_sources']

        for i in range(len(self.video_sources)):
            self.addVideoLabel(self.video_sources[i], i)
        
        
    
    
    def addVideoLabel(self, vid_source, idx):
        vid_frame = tk.Frame(self.scrollable.interior, borderwidth = 5, bg = 'white')
        vid_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10, expand = True, padx = 10)

        vid_label = tk.Label(vid_frame, text = "Video Path : {}".format(vid_source), font = 'Sans 11', bg = 'white')
        vid_button = FocusButton(vid_frame, in_color = '#049bc9', out_color = '#3A79D1', text = "Configure Lines", command = lambda idx = idx:self.drawLines( idx), fg = 'white', relief = tk.FLAT)
        del_button = FocusButton(vid_frame, in_color = '#f05454', out_color = '#c90404', text = "Delete", command = lambda idx = idx:self.deleteVid(idx), fg = 'white', relief = tk.FLAT)
        del_button.pack(side = tk.RIGHT, padx = 10)
        vid_button.pack(side = tk.RIGHT)
        vid_label.pack(side = tk.LEFT)
        self.vid_list.append(vid_frame)

    def drawLines(self, idx):
        idx = int(idx)
        video = Video(self.video_sources[idx], self.points_sources[idx])

        self.PaintApp = PaintApp(tk.Toplevel(self), video.getDrawFrame(), video.point_source )
        self.PaintApp.window.wm_attributes("-topmost", 1)

    def deleteVid(self, idx):
        pass
        # if messagebox.askokcancel("Delete", "Do you want to delete?", parent = self):
        #     try:
        #         self.config["video_sources"][idx] = None
        #         self.config["points_sources"][idx] = None
        #     except:
        #         pass


        #     self.vid_frames[idx].destroy()
        #     self.videos[idx] = None
        #     print(len(self.vid_frames))

    def addVidForm(self):
        self.vid_form = tk.Frame(self, borderwidth = 5, bg = '#3A79D1')
        self.vid_form.pack(side = tk.TOP, fill = tk.X, pady = 10, padx = 10, expand = False)

        self.vid_entry = PlaceholderEntry(self.vid_form, placeholder = 'Video Path', bg = 'white', font = 'Sans 11', width = 40, relief = tk.RAISED)
        self.vid_entry.pack(side = tk.LEFT, padx = 10)
        
        self.user_label = tk.Label( self.vid_form, text = 'Owner: ', font = 'Sans 11', bg = '#3A79D1', fg = 'white')
        self.user_label.pack(side = tk.LEFT)

        list_of_items = ["Cordell Cannata", "Lacey Naples", "Zachery Manigault", "Regan Brunt", "Mario Hilgefort", "Austin Phong", "Moises Saum", "Willy Neill", "Rosendo Sokoloff", "Salley Christenberry", "Toby Schneller", "Angel Buchwald", "Nestor Criger", "Arie Jozwiak", "Nita Montelongo", "Clemencia Okane", "Alison Scaggs", "Von Petrella", "Glennie Gurley", "Jamar Callender", "Titus Wenrich", "Chadwick Liedtke", "Sharlene Yochum", "Leonida Mutchler", "Duane Pickett", "Morton Brackins", "Ervin Trundy", "Antony Orwig", "Audrea Yutzy", "Michal Hepp", "Annelle Hoadley", "Hank Wyman", "Mika Fernandez", "Elisa Legendre", "Sade Nicolson", "Jessie Yi", "Forrest Mooneyhan", "Alvin Widell", "Lizette Ruppe", "Marguerita Pilarski", "Merna Argento", "Jess Daquila", "Breann Bevans", "Melvin Guidry", "Jacelyn Vanleer", "Jerome Riendeau", "Iraida Nyquist", "Micah Glantz", "Dorene Waldrip", "Fidel Garey", "Vertie Deady", "Rosalinda Odegaard", "Chong Hayner", "Candida Palazzolo", "Bennie Faison", "Nova Bunkley", "Francis Buckwalter", "Georgianne Espinal", "Karleen Dockins", "Hertha Lucus", "Ike Alberty", "Deangelo Revelle", "Juli Gallup", "Wendie Eisner", "Khalilah Travers", "Rex Outman", "Anabel King", "Lorelei Tardiff", "Pablo Berkey", "Mariel Tutino", "Leigh Marciano", "Ok Nadeau", "Zachary Antrim", "Chun Matthew", "Golden Keniston", "Anthony Johson", "Rossana Ahlstrom", "Amado Schluter", "Delila Lovelady", "Josef Belle", "Leif Negrete", "Alec Doss", "Darryl Stryker", "Michael Cagley", "Sabina Alejo", "Delana Mewborn", "Aurelio Crouch", "Ashlie Shulman", "Danielle Conlan", "Randal Donnell", "Rheba Anzalone", "Lilian Truax", "Weston Quarterman", "Britt Brunt", "Leonie Corbett", "Monika Gamet", "Ingeborg Bello", "Angelique Zhang", "Santiago Thibeau", "Eliseo Helmuth"]
        self.combobox = Combobox_Autocomplete(self.vid_form, list_of_items, relief = tk.RAISED, font = 'Sans 11', bg = 'white')
        self.combobox.pack(side = tk.LEFT)

        # self.user_entry = PlaceholderEntry(self.vid_form, placeholder = 'Owner', bg = 'white', font = 'Sans 11', width = 20, relief = tk.RAISED)
        # self.user_entry.pack(side = tk.LEFT, padx = 10)

        self.vid_form_btn = FocusButton(self.vid_form, in_color = '#32bf1d', out_color = '#149600', text = 'Add Video', relief = tk.FLAT, fg = 'white', command = self.addVideo)
        self.vid_form_btn.pack(side = tk.RIGHT)
    
    def addVideo(self):
        vid_path = self.vid_entry.get()
        self.vid_entry.clear()
        if len(vid_path) > 0:
            coord_path = "../datasets/coords{}_{}.yml".format(len(self.video_sources), random.randint(1, 100))
            
            video = Video(vid_path, coord_path)
            

            if video.getDrawFrame() is None:
                messagebox.showerror("Invalid Adress", "Invalid video source!, Please type again", parent = self)
                return

            self.video_sources.append(vid_path)
            self.points_sources.append(coord_path)

            self.addVideoLabel(video.video_source, len(self.video_sources) - 1)
            self.drawLines(len(self.video_sources) - 1)
            
            
    

    