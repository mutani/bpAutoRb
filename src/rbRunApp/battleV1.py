import pydirectinput
import pyautogui
import time
import threading
import random
import math

CONFIDENCE = 0.8
target_state_result = None
TARGET_IMAGE_FOLDER = "Image/targetImage/"
TARGET_ENABLE = TARGET_IMAGE_FOLDER + "rb_target_disenable.png"

def run_target_state(image_path, timeout=10):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        if time.time() - start_time > timeout:
            return None
        time.sleep(0.1)  # 待機時間を設ける

def run_target():
    pydirectinput.moveRel(random.randint(1300,1600), 0, duration=generate_random(0.1,0.3))
    pydirectinput.middleClick()

def run_main_attack():
    while True:
        #down
        pydirectinput.mouseDown()
        time.sleep(generate_random(0.05,0.1))
        pydirectinput.keyDown('e')
        time.sleep(generate_random(0.05,0.1))
        pydirectinput.keyDown('q')
        time.sleep(generate_random(0.05,0.1))
        #up
        pydirectinput.mouseUp()
        time.sleep(generate_random(0.05,0.1))
        pydirectinput.keyUp('e') 
        time.sleep(generate_random(0.05,0.1))
        pydirectinput.keyUp('q') 
        time.sleep(generate_random(0.05,0.1))

def battleRun():
    image_path = TARGET_ENABLE
    battleRun_thread = threading.Thread(target=run_main_attack)
    battleRun_thread.start()

    while True:
        if run_target_state(image_path):
            run_target()

def generate_random(least, highest):
    return math.floor(random.uniform(least, highest) * 100) / 100

