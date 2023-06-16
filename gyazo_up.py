import os
import time
import requests
from PIL import ImageGrab
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from dotenv import load_dotenv
load_dotenv()

desktop_dir = os.path.expanduser('~/Desktop')

class Screenshot():

    def __init__(self):
        self.screenshot_completion = False

    def on_created(self):

        image = ImageGrab.grabclipboard()

        if image is not None:
            time.sleep(1)  
            src_path = desktop_dir + "\\upload.png"
            image.save(src_path)
            self.upload_to_gyazo(src_path)
        else:
            return

    def upload_to_gyazo(self, filepath):

        ACCESS_TOKEN = os.getenv("gyazo_api")
        URL="https://upload.gyazo.com/api/upload"  

        headers = {'Authorization': "Bearer {}".format(ACCESS_TOKEN)}  

        with open(filepath, "rb") as f:  
            files = {'imagedata':f.read()}  

            response = requests.request('post', URL, headers=headers, files=files)  

            if response.status_code == 200:
                print("アップロード完了")

            textfilepath = desktop_dir + "\\url.txt"
            with open(textfilepath, "w") as f:
                f.write(response.json().get("url"))

            subprocess.run(["notepad.exe", textfilepath])
            self.screenshot_completion = True


if __name__ == "__main__":
    sch = Screenshot()
    print("スクリーンショットを撮ってください。")
    while True:
        sch.on_created()
        time.sleep(1)
        if sch.screenshot_completion:
            break
