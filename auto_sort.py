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
        # Track each specified directories
        for i in range(len(settings_data["analyze"])):
            # Checks each file in folder_to_track
            folder_to_track = settings_data["analyze"][i]["track"]
            for file in os.listdir(folder_to_track):
                # Not hidden file
                if file[0] != ".":
                    src = folder_to_track + "/" + file
                    _, file_extension = os.path.splitext(src)

                    # Sort to correct location
                    folder_dests = settings_data["analyze"][i]["dest"]
                    for j in range(len(folder_dests)):
                        current_extensions = settings_data["ext"][folder_dests[j]["ext"]].lower()
                        current_destination = folder_dests[j]["dest"]
                        correct_ext = False
                        
                        # Check if file match with current parameter, if it is a directory, chekcs if 1/3 of files in folder match with current parameters
                        if os.path.isdir(src):
                            correct_ext = check_folder(src, current_extensions)
                        elif file_extension.lower() in current_extensions.lower():
                            correct_ext = True
                        
                        new_name = file

                        # Assign folder destination
                        if correct_ext:
                            folder_destination = current_destination
                            new_destination = folder_destination + "/" + new_name
                            os.rename(src, new_destination)

homedir = os.environ['HOME']
with open('settings.json', 'r+') as file:
    content = file.read()
    file.seek(0)
    content_split = content.split("$")
    for i in range(1, len(content_split)-1, 2):
        content = content.replace('$' + content_split[i] + '$', os.environ[content_split[i]])
    settings_data = json.loads(content)

event_handler = MyHandler()
observer = Observer()

paths = [d["track"] for d in settings_data["analyze"]]

for i in paths:
    targetPath = str(i)
    observer.schedule(event_handler, targetPath, recursive=True)
    observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()