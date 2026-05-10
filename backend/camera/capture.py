import cv2
import time
from backend.config.settings import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, TARGET_FPS

class CameraCapture:
    def __init__(self):
        self.cap = None
        self.fps = 0
        self._prev_time = time.time()
        self._frame_count = 0

    def start(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)

        if not self.cap.isOpened():
            raise RuntimeError("could not open webcam!")
        
        print("camera is started SUKUNA-SAMA")


    def read_frame(self):
        success, bgr_frame = self.cap.read()
        if not success:
            return False, None, None
        

        bgr_frame = cv2.flip(bgr_frame, 1)
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        return True, bgr_frame, rgb_frame
    
    def stop(self):
        if self.cap:
            self.cap.release()
            print("camera stopped")