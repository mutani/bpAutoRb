import pydirectinput
import time
import rbRunApp.battleV1 as battle

def run_main_attack():
    while True:
        #down
        pydirectinput.mouseDown()
        time.sleep(battle.generate_random(0.05,0.1))
        pydirectinput.keyDown('e')
        time.sleep(battle.generate_random(0.05,0.1))
        pydirectinput.keyDown('q')
        time.sleep(battle.generate_random(0.05,0.1))
        #up
        pydirectinput.mouseUp()
        time.sleep(battle.generate_random(0.05,0.1))
        pydirectinput.keyUp('e') 
        time.sleep(battle.generate_random(0.05,0.1))
        pydirectinput.keyUp('q') 
        time.sleep(battle.generate_random(0.05,0.1))