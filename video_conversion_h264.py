import cv2
import os
import time
from threading import Thread as t
from functools import lru_cache
from queue import Queue

START = time.time()
INFO = '\033[0;32m[+INFO]:\033[0m'
ERROR = '\033[0;31m[ERROR]:\033[0m'
DEBUG = '\033[0;36m[DEBUG]:\033[0m'
MSG = '\033[1;33m[MSG]:\033[0m'

class video_converter():
    def __init__(self, videoPath:str, videoName=None):
        self.videoPath = videoPath
        self.vidq , self.framesize = self.read_video_queues()
        self.convert_to_mp4(self.vidq , self.framesize)

    @lru_cache(maxsize=128)
    def read_video_queues(self)->tuple:
        '''
        reads an input video file path and puts the frame in a seperate queue.'''
        
        if os.path.exists(self.videoPath):
            vid_queue = Queue()
            video = cv2.VideoCapture(self.videoPath)
            frame_size =  int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            start_time = time.time()
            while video.isOpened():
                reading, frame = video.read()
                if not reading:
                    break
                vid_queue.put(frame)
            reading_time = round(time.time()-start_time, 2)
            print(INFO+"Finished in {} s".format(reading_time))
            video.release()
            return vid_queue,frame_size
        
        else:
            print(DEBUG+'Input path does not exists.Exiting')
            exit()

    @lru_cache(maxsize=128)
    def convert_to_mp4(self, videoQueue:Queue, frame_size:tuple):

        '''
        writes the frame to a h264 VideoWriter container.'''

        if videoName == None:
            videoName = self.videoPath.split(os.path.sep)[-1].split('.')[0]+'.h264'
        
        fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
        video_writer = cv2.VideoWriter(videoName, fourcc , 30.0, frame_size)
        
        for num_of_frames in range(videoQueue.qsize()):
            frame = videoQueue.get()
            video_writer.write(frame)
        video_writer.release()

# mp4vid = video_converter(r'c:\Users\shash\Desktop\10_Most_Amazing_Patrol_Boats_in_the_World.mp4')
t1 = t(target=video_converter, args=(r'c:\Location\to\h264\vidfile.h264',))
t1.start()
t1.join()
full_time = round(time.time() - START,2)
print(INFO+'Finished in ',full_time)
