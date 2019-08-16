import tkinter as tk
import requests
import json
import random
import Errors
from tkinter import messagebox
from VideoCap import Video
from LineConfig import PaintApp
from Widgets import ClickableLabel, FocusButton, PlaceholderEntry, Combobox_Autocomplete, VerticalScrolledFrame


class CamerasFrame(tk.Frame):

    def __init__(self, parent, bg = '#3A79D1',  **kwargs):
        tk.Frame.__init__(self, parent, bg = bg, **kwargs)

        self.list_of_users = []
        self.list_of_ids = []
        
        self.scrollable = VerticalScrolledFrame(self, bg = 'white', **kwargs)
        self.scrollable.interior.configure(bg = 'white')
        self.scrollable.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        self.vid_list = []

        self.addVidForm()

        try:
            with open('config.json') as f:
                self.config = json.load(f)
                self.cameras = self.config['cameras']
        except:
            Errors.configNotFoundError()
            return

        for i in range(len(self.cameras)):
            self.addVideoLabel(self.cameras[i]['video_source'], self.cameras[i]['id'], self.cameras[i]['user'])
        
        
    def findCamera(self, idx):
        
        for i in range(len(self.cameras)):
            if(self.cameras[i]['id'] == idx):
                return i
        
        return -1
    
    def findByUser(self, username, show_all = False):
        for vid_frame in self.vid_list:
            vid_frame.pack_forget()
        
        if(show_all):
            for vid_frame in self.vid_list:
                vid_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10, expand = True, padx = 10)
        else:
            for vid_frame in self.vid_list:
                if(vid_frame.owner == username):
                    vid_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10, expand = True, padx = 10)


    def addVideoLabel(self, vid_source, idx, username):
        vid_frame = CamFrame(parent = self.scrollable.interior, owner = username, borderwidth = 5, bg = 'white')
        vid_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10, expand = True, padx = 10)

        vid_label = tk.Label(vid_frame, text = "Video Path : {}".format(vid_source), font = 'Sans 11', bg = 'white')
        username_label = tk.Label(vid_frame, text = "User: {}".format(username), font = 'Sans 11', bg = 'white')
        vid_button = FocusButton(vid_frame, in_color = '#049bc9', out_color = '#3A79D1', text = "Configure Lines", command = lambda idx = idx:self.drawLines( idx), fg = 'white', relief = tk.FLAT)
        del_button = FocusButton(vid_frame, in_color = '#f05454', out_color = '#c90404', text = "Delete", command = lambda idx = idx:self.deleteVid(idx), fg = 'white', relief = tk.FLAT)
        del_button.pack(side = tk.RIGHT, padx = 10)
        vid_button.pack(side = tk.RIGHT)
        vid_label.pack(side = tk.LEFT)
        username_label.pack(side = tk.LEFT, fill = tk.X, expand = True)
        self.vid_list.append(vid_frame)

    def drawLines(self, idx):
        id = self.findCamera(idx)
        video = Video(self.cameras[id]['video_source'], self.cameras[id]['line_source'])

        self.PaintApp = PaintApp(tk.Toplevel(self), video.getDrawFrame(), video.point_source )
        self.PaintApp.window.wm_attributes("-topmost", 1)

    def deleteVid(self, id):
        idx = self.findCamera(id)

        if messagebox.askokcancel("Delete", "Do you want to delete {}?".format(self.cameras[idx]['video_source']), parent = self):
            
            try:
                url = 'https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/camera/{}'.format(self.cameras[idx]['id'])
                with requests.Session() as session:
                    req = session.delete(url = url)
            except:
                Errors.networkConnectionError()
                return

            res = dict(req.json())

            if 'success' in res.keys():
                del self.cameras[idx]
                self.updateConfig()

                self.vid_list[idx].destroy()
                del self.vid_list[idx]

            else:
                Errors.unknownError()
                return

    def addVidForm(self):
        self.vid_form = tk.Frame(self, borderwidth = 5, bg = '#3A79D1')
        self.vid_form.pack(side = tk.TOP, fill = tk.X, pady = 10, padx = 10, expand = False)

        self.vid_entry = PlaceholderEntry(self.vid_form, placeholder = 'Video Path', bg = 'white', font = 'Sans 11', width = 40, relief = tk.RAISED)
        self.vid_entry.pack(side = tk.LEFT, padx = 10)
        
        self.user_label = tk.Label( self.vid_form, text = 'Owner: ', font = 'Sans 11', bg = '#3A79D1', fg = 'white')
        self.user_label.pack(side = tk.LEFT)

        list_of_items = self.list_of_users
        self.combobox = Combobox_Autocomplete(self.vid_form, list_of_items, relief = tk.RAISED, font = 'Sans 11', bg = 'white')
        self.combobox.pack(side = tk.LEFT)

        self.vid_form_btn = FocusButton(self.vid_form, in_color = '#32bf1d', out_color = '#149600', text = 'Add Video', relief = tk.FLAT, fg = 'white', command = self.addVideo)
        self.vid_form_btn.pack(side = tk.RIGHT)
    
    def addVideo(self):
        vid_path = self.vid_entry.get()
        self.vid_entry.clear()
        if len(vid_path) > 0:
            coord_path = "../datasets/coords{}_{}.yml".format(len(self.cameras), random.randint(1, 100))
            
            video = Video(vid_path, coord_path)
            

            if video.getDrawFrame() is None:
                Errors.invalidVideoAdress()
                return
            
            login = self.combobox.get_value()
            user_idx = -1
            for i in range(len(self.list_of_users)):
                if(self.list_of_users[i] == login):
                    user_idx = i

            if(user_idx >= 0):
                req = None

                try:
                    url = 'https://iguard-backend.herokuapp.com/api/v1/KDY7AehrzAlOVJd-i09GVA/register/camera?user_id={}'.format(self.list_of_ids[user_idx])
                    with requests.Session() as session:
                        req = session.post(url = url)

                except:
                    Errors.networkConnectionError()
                    return

                res = dict(req.json())
                if "errors" in res.keys():
                    error_text = ""
                    for error in res["errors"]:
                        error_text += error + "\n"
                    
                    messagebox.showerror("Error", error_text, parent = self)
                    return
                print(res)
            
                camera = {
                    'id' : res['id'],
                    'user' : login,
                    'video_source' : vid_path,
                    'line_source' : coord_path
                }
                self.cameras.append(camera)

                self.addVideoLabel(video.video_source, res['id'], login)
                self.drawLines(res['id'])
                self.updateConfig()
                
            
    def updateConfig(self):
        self.config['cameras'] = self.cameras

        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent = 5)

class CamFrame(tk.Frame):
    
    def __init__(self, parent, owner, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        self.owner = owner