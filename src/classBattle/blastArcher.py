import pydirectinput
import time
import rbRunApp.battleV1 as battle

def run_main_attack():
    while True:
        #down
        #Wキー土属性派生
        # pydirectinput.keyDown('w')
        pydirectinput.keyDown('d')
        pydirectinput.mouseDown()
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyDown('e')
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyUp('e') 
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyDown('q')
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyUp('q') 
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyDown('r')
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyUp('r')
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.mouseUp()
        time.sleep(battle.generate_random(0.03,0.06))
        pydirectinput.keyUp('w')
        # pydirectinput.keyUp('d')