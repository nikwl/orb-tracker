import cv2

from orb_tracker.ORBTracker import ORBTracker

class CameraObject():
    camera = cv2.VideoCapture(0)

    def get_frame(self):
        _, frame = cap.read()
        return frame

if __name__ == "__main__":
    c = CameraObject()
    lt = ORBTracker(c)
    
    while(True):
        annotated_frame, _ = lt.get_annotated_frame()
        if annotated_frame is not None:
            cv2.imshow('', annotated_frame)
            key = cv2.waitKey(delay=1)
            if key == ord('q'):
                break
