import os
import sys
import config
import multiprocessing as mp
import detector
import streamer
import viewer
from os import listdir
from os.path import isfile, join




def main():
    try:
        #Read all mp4 files from config folder
        video_files = [f for f in listdir(config.video_folder_path) if  f.endswith('.mp4')]
        for video_file in video_files:
            #Phase 1 - Creating 2 Queues for communication between processes
            detector_message_queue = mp.Queue()
            viewer_message_queue = mp.Queue()
            # Phase 1 - Creating 3 different objects
            streamer_object = streamer.Streamer(os.path.join(config.video_folder_path, video_file), detector_message_queue)
            detector_object = detector.Detector(detector_message_queue, viewer_message_queue)
            viewer_object = viewer.Viewer(viewer_message_queue)
            # Phase 1 - Creating 3 processes working with multiprocessing package
            streamer_process = mp.Process(target=streamer_object.run(), args=(video_file, detector_message_queue))
            detector_process = mp.Process(target=detector_object.run(), args=(detector_message_queue, viewer_message_queue))
            viewer_process = mp.Process(target=viewer_object.run(), args=(viewer_message_queue,))
            # Phase 1 - start 3 processes
            streamer_process.start()
            detector_process.start()
            viewer_process.start()
            # Phase 1 - wait for all processes will be finish
            streamer_process.join()
            detector_process.join()
            viewer_process.join()
            # Phase 3 - When the movie is finished  all process are terminated
            streamer_process.terminate()
            detector_process.terminate()
            viewer_process.terminate()
    except:
        print(f'Main exception occured {sys.exc_info()[0]}')


if __name__ == '__main__':
    main()
