from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

def check_folder(src, extension):
    correct_ext_in_folder = 0
    files_in_folder = 0
    for path in os.listdir(src):
        if os.path.isfile(os.path.join(src, path)):
            files_in_folder += 1
    for file_in_dir in os.listdir(src):
        if os.path.isfile(os.path.join(src, file_in_dir)):
            _, file_extension = os.path.splitext(src + "/" + file_in_dir)
            if file_extension.lower() in extension:
                correct_ext_in_folder += 1
                if correct_ext_in_folder >= files_in_folder // 2:
                    return True

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for i in range(len(settings_data["analyze"])):
            folder_to_track = homedir + settings_data["analyze"][i]["track"]
            for file in os.listdir(folder_to_track):
                src = folder_to_track + "/" + file
                _, file_extension = os.path.splitext(src)

                # Sort to correct location
                folder_dests = settings_data["analyze"][i]["dest"]
                for j in range(len(folder_dests)):
                    current_extensions = settings_data["ext"][folder_dests[j]["ext"]].lower()
                    current_destination = folder_dests[j]["dest"]
                    correct_ext = False
                    
                    if os.path.isdir(src):
                        correct_ext = check_folder(src, current_extensions)
                    elif file_extension.lower() in current_extensions.lower():
                        correct_ext = True
                    
                    # Assign folder destination
                    new_name = file

                    if correct_ext:
                        folder_destination = current_destination.replace("HOMEDIR", homedir)
                        new_destination = folder_destination + "/" + new_name
                        os.rename(src, new_destination)

homedir = os.environ['HOME']
with open('settings.json') as json_file:
    settings_data = json.load(json_file)

event_handler = MyHandler()
observer = Observer()

paths = [d["track"].replace("HOMEDIR", homedir) for d in settings_data["analyze"]]
for i in paths:
    targetPath = i
    observer.schedule(event_handler, targetPath, recursive=True)
    observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()