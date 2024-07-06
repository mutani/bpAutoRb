import pydirectinput
import pyautogui
import time
import threading
import random
import math
import classBattle.blitzLancer as blitzLancerBattle
import classBattle.blastArcher as blastArcherBattle

CONFIDENCE = 0.6
TARGET_IMAGE_FOLDER = "Image/targetImage/"
TARGET_ENABLE = TARGET_IMAGE_FOLDER + "rb_target_disenable.png"
BLITZLANCERBATTLE = "blitzLancer"
BLASTARCHERBATTKE = "blastArcher"

def battleRun(arg_class):
    image_path = TARGET_ENABLE
    if arg_class == BLITZLANCERBATTLE:
        battleRun_thread = threading.Thread(target=blitzLancerBattle.run_main_attack)
    elif arg_class == BLASTARCHERBATTKE:
        battleRun_thread = threading.Thread(target=blastArcherBattle.run_main_attack)
    else:
        battleRun_thread = threading.Thread(target=blitzLancerBattle.run_main_attack)

    battleRun_thread.start()

    while True:
        if run_target_state(image_path):
            run_target()

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
        time.sleep(0.1)

def run_target():
    pydirectinput.moveRel(random.randint(1300,1600), 0, duration=generate_random(0.1,0.3))
    pydirectinput.middleClick()

def generate_random(least, highest):
    return math.floor(random.uniform(least, highest) * 100) / 100

