import tkinter as tk
import platform
import PIL.Image, PIL.ImageTk
from Widgets import ClickableLabel, BlinkingLabel, VerticalScrolledFrame
from tkinter import messagebox
from VideoCap import Video
from newVideoCap import MyVideoCapture
from HumanDetection import DetectorAPI
from database import Database
from Notifications import Notifications
import multiprocessing
import json
import cv2
# import asyncio
# import aiohttp
import requests
import concurrent.futures
import threading

# async def makeRequest(session, url, params):
#     print(params)
#     async with session.post(url, data = params) as response:
#         print("Response : {}".format(response.text))
#         params['picture'].close()
#     print("hello")

# async def makeManyRequests(rows):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for row in rows:
#             url = "https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/notifications"
#             (_, cam_id, filepath, _, _) = row
#             params = {
#                 'camera_id' : cam_id,
#                 'picture' : open(filepath, 'rb')
#             }
#             task = asyncio.ensure_future(makeRequest(session, url, params))
#             tasks.append(task)
#         await asyncio.gather(*tasks, return_exceptions=True)

thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def send_row(row):
    session = get_session()
    url = "https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/notifications"
    (_, cam_id, filepath, _, _) = row
    data = {
        'camera_id' : cam_id,
    }

    files = {
        'picture' : open(filepath, 'rb')
    }

    with session.post(url, data = data, files = files) as response:
        print(response.text)


def send_all_rows(rows):
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        executor.map(send_row, rows)



class GuestApp(tk.Tk):

    def __init__(self, restart_var):
        # self.async_loop = asyncio.get_event_loop()

        tk.Tk.__init__(self)
        self.restart_var = restart_var
        
        self.window_config = {
            "title" : "IGuard Desktop",
            "bg_color" : "white",
            "quit_text" : "Do you want to quit ?",
            "alerts_label" : "Alerts",
            "cameras-text" : "Cameras",
            'alert_cam_text' : "Violation detected on this camera (click here to close)" 
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
        self.main_vid_frame = tk.Frame(self.panedwindow, relief = tk.FLAT, bg = 'white')
        self.alert_frame = VerticalScrolledFrame(self.panedwindow, relief = tk.FLAT, bg = self.window_config["bg_color"])
        
        self.vid_frame = tk.Frame(self.main_vid_frame)
        self.vid_frame.pack(side = tk.TOP, fill = tk.X)

        self.alert_cam_label = None

        # model_path = './faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
        # self.odapi = DetectorAPI(path_to_ckpt=model_path)

        # self.load_video()
        self.video_width = int(0.65 * screen_width)
        self.panedwindow.add(self.list_frame, width = int(0.2 * screen_width))
        self.panedwindow.add(self.main_vid_frame, width = int(0.65 * screen_width))
        self.panedwindow.add(self.alert_frame)

        self.loadVideo()
        self.loadNotifications()
        
        self.delay = 1

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # self.analyze_process =  multiprocessing.Process(target = analyze)
        # self.analyze_process.start()

        self.updateVid()

        self.check_alert()
        
    
    def loadVideo(self):
        try:
            with open('config.json') as f:
                self.config = json.load(f)
        except:
            messagebox.showerror("Error", "Couldn't fint config.json. Please, contact to developers !")
            return
        cameras = self.config["cameras"]
        
        label = tk.Label(self.list_frame.interior, text = self.window_config['cameras-text'])
        label.pack(side = tk.TOP, fill = tk.X)
        self.video_list = []
        self.videos = []

        for i, camera in enumerate(cameras):
            video_text = camera['video_source'].split("/")[-1]
            label = ClickableLabel(self.list_frame.interior, in_color = '#005673', out_color = '#3A79D1', clicked_color = self.window_config['bg_color'], text = video_text, font = "Arial 13", heigh = 5)
            label.bind("<Button-1>", lambda e, i = i : self.vidListCommand(i))
            label.pack(side = tk.TOP, fill = tk.X)
            self.video_list.append(label)
            # self.videos.append( Video(camera['video_source'], camera['line_source'], camera['id']) )
            self.videos.append([camera['video_source'], camera['line_source'], camera['id']])
            # self.videos.append(camera)

        self.on_screen = -1
        if(len(self.video_list) > 0):
            self.vidListCommand(0)
        
        self.panel = tk.Label(self.vid_frame, bg = "#3A79D1")
        self.panel.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        
    def vidListCommand(self, idx):
        if(idx == self.on_screen):
            return

        if(self.on_screen >= 0 ):
            self.video_list[self.on_screen].click()
        self.video_list[idx].click()

        self.on_screen = idx
        self.capp = Video(self.videos[idx][0], self.videos[idx][1], self.videos[idx][2])
        if self.alert_cam_label:
            self.alert_cam_label.destroy()
        # self.capp = MyVideoCapture(self.videos[idx], self.config, self.odapi)

    def updateVid(self):
        # frame = self.videos[self.on_screen].getFrame()
        frame = self.capp.getFrame()

        if(frame is not None):
            self.update()
            #width = self.main_vid_frame.winfo_width()
            width = self.video_width
            (cols, rows, _) = frame.shape
            # print(width, cols, rows)
            frame = cv2.resize(frame, (width, int(cols / rows * width)))

            img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.panel.configure(image = img)
            self.panel.image = img

        self.vid_after_id = self.panel.after(self.delay, self.updateVid)

    def on_closing(self):
        if messagebox.askokcancel("Quit", self.window_config['quit_text']):
            self.after_cancel(self.alert_after_id)
            self.panel.after_cancel(self.vid_after_id)
            # self.analyze_process.terminate()
            self.destroy()
            self.restart_var[0] = True
        

    def loadNotifications(self):
        self.db = Database("alert_db.db")
        self.notes = []
        self.alert_label = tk.Label(self.alert_frame.interior, text = self.window_config['alerts_label'])
        self.alert_label.pack(side = tk.TOP)
        all_data = self.db.select_all()
        self.row_number = len(all_data)
        for data in all_data:
            note = Notifications(self.alert_frame.interior, self.db, db_data = data)
            note.button.pack(expand = 1, side = tk.BOTTOM)
            self.notes.append(note)
        

    def check_alert(self):
        data_rows = self.db.select_with_offset(self.row_number)
        new_rows = []
        for row in data_rows:
            self.row_number += 1
            note = Notifications(self.alert_frame.interior, self.db, db_data = row)
            new_rows.append(row)
            note.button.pack(expand = 1, side = tk.BOTTOM)
            self.notes.append(note)
        
        if(len(new_rows) > 0):
            self.alertOnCam(data_rows[-1][1])
            send_all_rows(new_rows)
            # future = asyncio.ensure_future(makeManyRequests(new_rows))
            # self.async_loop.run_until_complete(future)

        self.alert_after_id = self.after(1000, self.check_alert)
        
    


    def alertOnCam(self, id):
        idx = -1
        for i in range(len(self.videos)):
            if(self.videos[i][2] == id):
                idx = i
                break
        if(idx == -1):
            return
        print(idx)    
        self.vidListCommand(idx)
        
        if not self.alert_cam_label:
            self.alert_cam_label = BlinkingLabel(self.vid_frame, first_color = '#ff3838', second_color = '#871a1a', text = self.window_config['alert_cam_text'], fg = 'white', font = 'Sans 13', height = 3)
            self.alert_cam_label.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
            self.alert_cam_label.bind("<Button-1>", lambda e : self.alert_cam_label.destroy())
            # alert_cam_label.after(15000, alert_cam_label.destroy)