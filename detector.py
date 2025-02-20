import sys
import cv2
from base_command import BaseCommand

class Detector(BaseCommand):
    def __init__(self, detectorMessageQueue,ViewerMessageQueue):
        self.detector_message_queue = detectorMessageQueue
        self.viewer_message_queue = ViewerMessageQueue

    def run(self):
        try:
            while True:
                #Get the frame from the message queue
                frame = self.detector_message_queue.get()
                if frame is None:
                    self.viewer_message_queue.put((None, None))
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (21, 21), 0)
                _, thresh = cv2.threshold(blurred, 25, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                detections = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 500]
                #Save the frame in viewer message queue
                self.viewer_message_queue.put((frame, detections))
        except:
            print(f'Detector exception occured: {sys.exc_info()[0]}')
