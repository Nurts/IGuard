import tkinter as tk
import platform
import PIL.Image, PIL.ImageTk
from VerticalScrolledFrame import VerticalScrolledFrame
from Widgets import ClickableLabel
from tkinter import messagebox
from VideoCap import Video
from database import Database
from Notifications import Notifications
import json
import cv2

class GuestApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        
        self.window_config = {
            "title" : "IGuard Desktop",
            "bg_color" : "white",
            "quit_text" : "Do you want to quit ?",
            "alerts_label" : "Here are the alerts"
        }

        self.title(self.window_config["title"])
        self.configure(bg = self.window_config["bg_color"])

        if platform.system() == "Windows":
            self.state('zoomed')
        else:
            self.state('iconic')
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("{}x{}".format(screen_width, screen_height))


        self.panedwindow = tk.PanedWindow(self, orient = tk.HORIZONTAL, sashwidth = 5, sashrelief = tk.RAISED, bg = self.window_config["bg_color"])
        self.panedwindow.pack(fill = tk.BOTH, expand = True)
        
        self.list_frame = VerticalScrolledFrame(self.panedwindow, relief = tk.FLAT, bg = self.window_config["bg_color"])
        self.vid_frame = VerticalScrolledFrame(self.panedwindow, relief = tk.FLAT, bg = self.window_config["bg_color"])
        self.alert_frame = VerticalScrolledFrame(self.panedwindow, relief = tk.FLAT, bg = self.window_config["bg_color"])
        
        self.loadVideo()
        self.loadNotifications()

        # self.load_video()

        self.panedwindow.add(self.list_frame, width = int(0.2 * screen_width))
        self.panedwindow.add(self.vid_frame, width = int(0.65 * screen_width))
        self.panedwindow.add(self.alert_frame)

        self.delay = 1

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.updateVid()

        self.check_alert()
        
    
    def loadVideo(self):
        with open('config.json') as f:
            self.config = json.load(f)
        
        video_sources = self.config["video_sources"]
        points_sources = self.config["points_sources"]

        self.video_list = []
        self.videos = []

        for i, video_source in enumerate(video_sources):
            video_text = video_source.split("/")[-1]
            label = ClickableLabel(self.list_frame.interior, in_color = '#005673', out_color = '#3A79D1', clicked_color = self.window_config['bg_color'], text = video_text, font = "Arial 13", heigh = 5)
            label.bind("<Button-1>", lambda e, i = i : self.vidListCommand(i))
            label.pack(side = tk.TOP, fill = tk.X)
            self.video_list.append(label)
            self.videos.append( Video(video_source, points_sources[i]) )

        self.on_screen = -1
        if(len(self.video_list) > 0):
            self.vidListCommand(0)
        
        self.panel = tk.Label(self.vid_frame.interior, bg = "#3A79D1")
        self.panel.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
    def vidListCommand(self, idx):
        if(idx == self.on_screen):
            return

        if(self.on_screen >= 0 ):
            self.video_list[self.on_screen].click()
        self.video_list[idx].click()

        self.on_screen = idx

    def updateVid(self):
        frame = self.videos[self.on_screen].getFrame()

        if(frame is not None):
            self.update()
            width = self.panel.winfo_width()
            (cols, rows, _) = frame.shape
            frame = cv2.resize(frame, (width, int(cols / rows * width)))

            img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.panel.configure(image = img)
            self.panel.image = img

            self.after(self.delay, self.updateVid)

    def on_closing(self):
        if messagebox.askokcancel("Quit", self.window_config['quit_text']):
            self.destroy()
        

    def loadNotifications(self):
        self.db = Database("alert_db.db")
        self.notes = []
        self.alert_label = tk.Label(self.alert_frame.interior, text = self.window_config['alerts_label'])
        self.alert_label.pack(side = tk.TOP)
        all_data = self.db.select_all()
        self.row_number = len(all_data)
        for i, data in enumerate(all_data):
            note = Notifications(self.alert_frame.interior, self.db, from_db = True, db_data = data)
            note.button.pack(expand = 1, side = tk.BOTTOM)
            self.notes.append(note)
        

    def check_alert(self):
        data_rows = self.db.select_with_offset(self.row_number)
        
        for row in data_rows:
            self.row_number += 1
            note = Notifications(self.alert_frame.interior, self.db, from_db = True, db_data = row)
            note.button.pack(expand = 1, side = tk.BOTTOM)
            self.notes.append(note)       
        
        self.after(1000, self.check_alert)

    