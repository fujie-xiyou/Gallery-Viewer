import logging
import os
import time
import typing

from pynput.keyboard import Key, Listener, KeyCode
from playsound import playsound
import pyperclip
import requests
import tkinter

from PIL import ImageGrab

logging.basicConfig(level=logging.INFO)

win = tkinter.Tk()
width = win.winfo_screenwidth()
height = win.winfo_screenheight()

key_hist: typing.Dict[KeyCode, float] = {}


def is_double_paress(key: KeyCode, expect, delay=0.2):
    if key != expect:
        return False
    last_time = key_hist.get(key)
    now = time.time()
    key_hist[key] = now
    if last_time is None:
        return False
    return now - last_time <= delay


def on_press(key: KeyCode):
    if key == Key.ctrl_r or key == Key.cmd_r:
        try:
            resp = requests.get(f"http://{HOST}/load_connect")
            data = resp.json()["data"]
        except Exception as e:
            logging.exception("获取内容失败 e=%s", e)
            return
        pyperclip.copy(data)
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S"))

    if is_double_paress(key, Key.alt_r):
        img = ImageGrab.grab(bbox=(0, 0, width, height))
        path = os.environ.get("HOME") + "/Desktop/screenshot/"
        os.makedirs(path, exist_ok=True)
        img.save(path + time.strftime("%Y年%m月%d日 %H时%M分%S秒") + ".png")
        img.close()
        playsound("static/kacha.mp3")


HOST = "127.0.0.1"


def start(host):
    global HOST
    HOST = host
    Listener(on_press=on_press).start()
    logging.info("clip启动完成")

