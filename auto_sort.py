from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

def check_folder(src, extension, match_precent=50):
    match_in_folder = 0
    files_in_folder = 0
    for path in os.listdir(src):
        if os.path.isfile(os.path.join(src, path)):
            files_in_folder += 1
    for file_in_dir in os.listdir(src):
        if os.path.isfile(os.path.join(src, file_in_dir)):
            _, file_extension = os.path.splitext(src + "/" + file_in_dir)
            if file_extension.lower() in extension:
                match_in_folder += 1
                if match_in_folder >= files_in_folder * match_precent/100:
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
                        current_ext_dict = settings_data["ext"][folder_dests[j]["ext"]]
                        current_ext = current_ext_dict["ext"].lower()
                        current_destination = folder_dests[j]["dest"]
                        match = False
                        
                        # Check if file match with current parameter, if it is a directory, chekcs if 1/3 of files in folder match with current parameters
                        if os.path.isdir(src):
                            try: 
                                check_folder = current_ext_dict["check_folder"]
                                try:
                                    match = check_folder(src, current_ext, current_ext_dict["match_precent"])
                                except:
                                    match = check_folder(src, current_ext)
                            except:
                                pass
                        elif file_extension.lower() in current_ext.lower():
                            match = True
                        
                        new_name = file

                        # Assign folder destination
                        if match:
                            folder_destination = current_destination
                            new_destination = folder_destination + "/" + new_name
                            os.rename(src, new_destination)

homedir = os.environ['HOME']
with open(os.path.dirname(os.path.realpath(__file__)) + '/settings.json') as file:
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