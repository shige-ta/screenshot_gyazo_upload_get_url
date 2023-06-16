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
        self.flg = False

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

        # 1.アクセストークンを含んだヘッダー情報を作成
        headers = {'Authorization': "Bearer {}".format(ACCESS_TOKEN)}  

        # 2.アップロードする画像をロード
        with open(filepath, "rb") as f:  
            # 3.画像のバイナリをキー（imagedata）にセット  
            files = {'imagedata':f.read()}  

            # 通信開始  
            response = requests.request('post', URL, headers=headers, files=files)  

            # HTTPステータスコードを取得  
            if response.status_code == 200:
                print("アップロード完了")

            textfilepath = desktop_dir + "\\url.txt"
            # テキストファイルを作成し、URLを書き込む
            with open(textfilepath, "w") as f:
                f.write(response.json().get("url"))

            # Notepadでテキストファイルを開く
            subprocess.run(["notepad.exe", textfilepath])
            self.flg = True


if __name__ == "__main__":
    sch = Screenshot()
    print("スクリーンショットを撮ってください。")
    while True:
        sch.on_created()
        time.sleep(1)
        if sch.flg:
            break
