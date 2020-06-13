# orb-tracker #

## Overview ##
This is modified version of an existing implementation of an ORB object tracker by [Alberto Serrano & Stephen Kim](https://github.com/ascalva/ORB-Object-Tracker). I found their implementation very useful but didn't like the front end. This is a lightweight redesign of the implementation such that it can be tacked on to other projects easily.

The front end is designed such that you can easily change the camera depending on your application. To do so simply create a class around the camera and implement a get_frame function. If you're interested in using the kinect camera with this tracker, check out my [kinect-toolbox](https://github.com/nikwl/kinect-toolbox). 

## Installation ##
Tested with python2.7 and python3.6.
1) Install required python packages:
     ```bash
     pip install -r requirements.txt
     ```
2) Test installation:
     ```bash
     python test.py
     ```

## Usage
```python
import cv2

from orb_tracker.orb_tracker import ORBTracker

class CameraObject():
    cap = cv2.VideoCapture(0)

    def get_frame(self):
        _, frame = self.cap.read()
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

```