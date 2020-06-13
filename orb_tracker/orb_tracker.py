import threading
import cv2

# Local imports
from .tracker import processLiveFeed, processLiveFeedPerm

"""
Implements an ORB-based object tracker as specified by the paper:
   Object Tracking Based on ORB and Temporal-Spacial Constraint by Shuang Wu,
   IEEE Student Member, Yawen Fan, Shibao Zheng, IEEE Member and Hua Yang, IEEE
   Member

Authors: Alberto Serrano, Stephen Kim
"""

class ORBTracker(threading.Thread):
    def __init__(self, camera):
        threading.Thread.__init__(self) 
        self.daemon = True

        self.camera = camera

        self.annotated_frame = None

        self.frame_lock = threading.Lock()

        self.set_tracker()

        self.start()

    def set_tracker(self):
        with self.frame_lock:
            img = self.camera.get_frame()
            
            # prompt for ROI, then set to cframe
            bbox = cv2.selectROI(img, True)
            self.prevImg = img
            cv2.destroyAllWindows()

            # Extract Bounding Box features
            x   = int(bbox[0])
            y   = int(bbox[1])
            w   = int(bbox[2])
            h   = int(bbox[3])
            x_i = x + w/2
            y_i = y + h/2

            # Define current and past frame
            self.cframe = (x_i, y_i, w, h)
            self.pframe = self.cframe[:]

    def run(self): 
        
        kp1, des1 = None, None
        
        with self.frame_lock:
            prevImg = self.prevImg
            pframe = self.pframe
            cframe = self.cframe

        while(True):
            # Capture frame-by-frame
            img = self.camera.get_frame()

            # prevImg will be None for first iteration (first frame)
            pframe, cframe, kp1, des1, annotated_frame = processLiveFeedPerm(prevImg, img, self.pframe, self.cframe, kp1, des1)

            prevImg = img

            with self.frame_lock:
                self.prevImg = prevImg
                self.pframe = pframe
                self.cframe = cframe
                self.annotated_frame = annotated_frame

        # When everything done, release the capture
        cv2.destroyAllWindows()

    def get_annotated_frame(self):
        with self.frame_lock:
            return self.annotated_frame, self.cframe