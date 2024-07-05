import rbRunApp.battleV1 as battle

import cv2
import pyautogui
import numpy as np
import pygetwindow as gw
import time
import tkinter as tk
import multiprocessing
import pydirectinput
import random
from tkinter import messagebox
from PIL import ImageGrab
from mss import mss
from multiprocessing import Process, Event

WINDOWTITLE = "BLUE PROTOCOL"
CONFIDENCE = 0.8
TARGET_IMAGE_FOLDER = "Image/targetImage/"
COMMAND_MENU_MISSION = TARGET_IMAGE_FOLDER + "0_mission_command_menu.png"
RETIRE = TARGET_IMAGE_FOLDER + "0_retire.png"
RETIRE_CONFIRM = TARGET_IMAGE_FOLDER + "0_retire_confirm.png"
MENU_RUSH = TARGET_IMAGE_FOLDER + "1_category_rush_command_menu.png"
#select mission
MISSION_RUSH1 = TARGET_IMAGE_FOLDER + "2_mission_rush1.png"
MISSION_RUSH3 = TARGET_IMAGE_FOLDER + "2_mission_rush3.png"
MISSION_RUSH4 = TARGET_IMAGE_FOLDER + "2_mission_rush4.png"
SOLO_MATCHING = TARGET_IMAGE_FOLDER + "3_solo_matching.png"
GOING_TO_BATTLE = TARGET_IMAGE_FOLDER + "4_going_matching.png"
BATTLE_START = TARGET_IMAGE_FOLDER + "5_battle_start.png"
EXIT_MATCH = TARGET_IMAGE_FOLDER + "exit_match.png"
TELEPORTER = TARGET_IMAGE_FOLDER + "teleporter.png"


def rbRun():
    windowState = capture_process_window(WINDOWTITLE,False)
    if windowState == False:
        return
    
    #roop
    while True:
        pyautogui.press('m')
        pyautogui.sleep(1)
        pyautogui.press('k')
        pyautogui.sleep(1)
        if find_button_and_click(WINDOWTITLE, MENU_RUSH) == False:
            continue
        find_button_and_click(WINDOWTITLE, MISSION_RUSH3)
        find_button_and_click(WINDOWTITLE, SOLO_MATCHING)
        root = tk.Tk()
        root.withdraw() 
        if wait_for_image_to_appear(GOING_TO_BATTLE):
            find_button_and_click(WINDOWTITLE, GOING_TO_BATTLE)
        else:
            messagebox.showinfo("error", "error: battle not found")
        #　battle start画像が出るまで待機
        if wait_for_image_to_appear(BATTLE_START, timeout=90):
            battle_end_event = Event()
            process = multiprocessing.Process(target=run_battle, args=(battle_end_event,))
            process.start()
            while True:
                if wait_for_image_to_appear(EXIT_MATCH):
                    print('exit match')
                    process.terminate()
                    break
            process.join()
            find_button_and_click(WINDOWTITLE, EXIT_MATCH)
            time.sleep(battle.generate_random(1,3))
            if wait_for_image_to_appear(EXIT_MATCH, timeout=3):
                print('exit matchできてないよ')
                for i in range(4):
                    pydirectinput.moveRel(random.randint(10,20), 0, duration=0.3)
                    pydirectinput.click()
                    time.sleep(battle.generate_random(0.2,0.4))
                time.sleep(battle.generate_random(1,3))
            wait_for_image_to_appear(TELEPORTER, timeout=35)
        #リタイア処理
        else:
            pyautogui.press('k')
            find_button_and_click(WINDOWTITLE, RETIRE)
            find_button_and_click(WINDOWTITLE, RETIRE_CONFIRM)
            messagebox.showinfo("error", "error: battle not found")

def run_battle(battle_end_event):
    battle.battleRun()
    if battle_end_event.is_set():
        return  # ここで処理を終了

def find_button_and_click(window_title, button_image_path, timeout=5):
    # ウィンドウのハンドルを取得
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()
    pyautogui.sleep(0.4)  # ウィンドウがアクティブになるのを待つ
    start_time = time.time()
    with mss() as sct:
        # モニターの情報を取得
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        while True:
            # ウィンドウの画像をリアルタイムでキャプチャ
            img = np.array(sct.grab(monitor))
            # BGRからRGBへ変換
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # ボタンの位置を特定するためにテンプレート画像をグレースケールで読み込む
            button_img = cv2.imread(button_image_path, cv2.IMREAD_GRAYSCALE)

            # 入力画像もグレースケールに変換
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # テンプレートマッチングを実行
            result = cv2.matchTemplate(img, button_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > CONFIDENCE:  # 類似度が閾値以上の場合
                # ボタンの中心を計算
                button_center = (max_loc[0] + button_img.shape[1] // 2, max_loc[1] + button_img.shape[0] // 2)
                screen_x, screen_y = window.left + button_center[0], window.top + button_center[1]
                # ボタンをクリック
                pyautogui.moveTo(screen_x, screen_y, duration=0.3)
                time.sleep(0.1)
                pyautogui.click(screen_x, screen_y)
                break

            if time.time() - start_time > timeout:
                print("find_button_and_click:Timeout reached, image not found.:" + button_image_path)
                return False

def wait_for_image_to_appear(image_path, timeout=30):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            # 画像が見つからない場合の処理
            pass

        if time.time() - start_time > timeout:
            print("wait_for_image:Timeout reached, image not found.:" + image_path)
            return None
        time.sleep(0.1)  # 待機時間を設ける

def capture_process_window(title_substring, screenshot=True):
    """
    指定されたタイトルの部分文字列を含むウィンドウのスクリーンショットを取得します。

    :param title_substring: ウィンドウタイトルの部分文字列
    :return: PIL Imageオブジェクト
    """
    # タイトルに部分文字列を含むウィンドウを検索
    windows = gw.getWindowsWithTitle(title_substring)
    if windows:
        window = windows[0]  # 最初に見つかったウィンドウを使用
        if window.isMinimized:  # ウィンドウが最小化されているか確認
            window.restore()  # 最小化されている場合は復元
        window.activate()  # ウィンドウをアクティブにする

        if screenshot == False:
            return None

        # ウィンドウの境界を取得
        left, top, right, bottom = window.left, window.top, window.right, window.bottom

        # スクリーンショットを取得
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        return screenshot
    else:
        print(f"No window found with title substring: {title_substring}")
        return False
