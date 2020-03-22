from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

class MyHandler(FileSystemEventHandler):
    i = 1
    def on_modified(self, event):
        # new_name = "new_file_" + str(self.i) + ".txt"
        for file in os.listdir(folder_to_track):
            # file_exists = os.path.isfile(folder_destination + "/" + new_name)
            # while file_exists:
            #     self.i += 1
            #     new_name = "new_file_" + str(self.i) + ".txt"
            #     file_exists = os.path.isfile(folder_destination + "/" + new_name)

            src = folder_to_track + "/" + file
            filename, file_extension = os.path.splitext(src)
            
            # Sort to different locations

            is_image = False
            is_dir = os.path.isdir(src)
            if is_dir:
                images_in_folder = 0
                files_in_folder = 0
                for path in os.listdir(src):
                    if os.path.isfile(os.path.join(src, path)):
                        files_in_folder += 1
                for file_in_dir in os.listdir(src):
                    if os.path.isfile(src + "/" + file_in_dir):
                        filename, file_extension = os.path.splitext(src + "/" + file_in_dir)
                        if file_extension in imageExtensions:
                            images_in_folder += 1
                            if images_in_folder >= files_in_folder // 2:
                                is_image = True
                                break
            elif file_extension in imageExtensions:
                is_image = True
            
            # Assign folder destination
            new_name = file
            #if not is_dir:
            #    new_name += file_extension

            if is_image:
                folder_destination = homedir + "/Pictures"
                new_destination = folder_destination + "/" + new_name
                os.rename(src, new_destination)

homedir = os.environ['HOME']
folder_to_track = homedir + "/Downloads"
folder_destination = "/Users/henrik/Desktop/dest"
imageExtensions = ".jpg.jpeg.png.gif"

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()