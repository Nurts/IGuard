import cv2
import numpy as np
import tkinter
import PIL.Image, PIL.ImageTk
import os
import yaml


class Video:

    def __init__(self, video_source, point_source, cam_id):
        self.cam_id = cam_id
        self.video_source = video_source
        self.point_source = point_source
        
        self.cap = cv2.VideoCapture(self.video_source)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        self.lines = []

        try:
            with open(self.point_source, 'r') as stream:
                line_data = yaml.load(stream)

                for idx in line_data:
                    self.lines.append(line_data[idx])
        except:
            pass
        
        print("Video streaming started cam {}".format(video_source))
        
    def getDrawFrame(self):
        ret, frame = self.cap.read()
        if ret == False:
            return None
        for line in self.lines:
            li_x, li_y = (line[0], line[1]), (line[2], line[3])
            cv2.line(frame, li_x, li_y, (255,0,0), 2)
        return frame
        

    def getFrame(self):
        try:
            for j in range(4):
                self.cap.grab()
            ret, frame_out = self.cap.read()
            if not ret:
                self.cap.release()
                self.cap = cv2.VideoCapture(self.video_source)
                return None
            else:
                return frame_out
        except:
            print("getFrame error")
            return None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()