from base_command import BaseCommand
import cv2

class Streamer(BaseCommand):
    def __init__(self, fileName, detectorMessageQequeue):
        self.file_name = fileName
        self.detector_message_queue = detectorMessageQequeue

    def run(self):
        try:
            cap = cv2.VideoCapture(self.file_name)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    #Saved the frame into detector message queue
                self.detector_message_queue.put(frame)
            cap.release()
            #Save the end of the stream into detector message queue
            self.detector_message_queue.put(None)
        except:
            print(f'Streamer exception when reading {self.file_name}')
