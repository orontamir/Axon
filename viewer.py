import sys
import time
import matplotlib.pyplot as plt
import cv2

from base_command import BaseCommand

class Viewer(BaseCommand):
    def __init__(self, ViewerMessageQueue):
        self.viewer_message_queue = ViewerMessageQueue
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.img_plot = None

    def run(self):
        try:
            while True:
                data = self.viewer_message_queue.get()
                if data[0] is None:
                    break
                frame, detections = data
                if frame is None:
                    print("Received None frame")
                    continue
                for (x, y, w, h) in detections:
                    #Phase 2 - Add Blurring algorithm
                    roi = frame[y:y + h, x:x + w]
                    blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)
                    frame[y:y + h, x:x + w] = blurred_roi
                    # Phase 1 - Draw rectangle for visualization
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                current_time = time.strftime("%H:%M:%S", time.localtime())
                # Phase 1 - Add current time in the left corner
                cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.img_plot is None:
                    self.img_plot = self.ax.imshow(frame_rgb)
                else:
                    self.img_plot.set_data(frame_rgb)
                plt.pause(0.001)
            plt.ioff()
            plt.show()
        except :
            print(f' Viewer exception occured: {sys.exc_info()[0]}')
