import pyautogui
import time
import threading
from pynput import keyboard

stop_playback = False

time.sleep(5)

def on_press(key):
    global stop_playback
    if key == keyboard.Key.backspace:
        stop_playback = True
        return False

def playback_movements():
    global stop_playback
    while not stop_playback:
        start_time = movements[0][-1]
        for movement in movements:
            if stop_playback:
                break
            event_time = movement[-1]
            time.sleep(event_time - start_time)
            
            if movement[0] == 'mouse':
                if movement[1] == 'click':
                    if movement[3]:  # pressed
                        pyautogui.mouseDown(x=movement[4], y=movement[5], button=movement[2])
                    else:  # released
                        pyautogui.mouseUp(x=movement[4], y=movement[5], button=movement[2])
                elif movement[1] == 'move':
                    pyautogui.moveTo(movement[2], movement[3])
                elif movement[1] == 'scroll':
                    pyautogui.scroll(movement[2], x=movement[3], y=movement[4])
            elif movement[0] == 'keyboard':
                if movement[1] == 'press':
                    pyautogui.keyDown(movement[2])
                elif movement[1] == 'release':
                    pyautogui.keyUp(movement[2])
            
            start_time = event_time

movements = []
with open('movements.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()
        if parts[0] == 'mouse':
            if parts[1] == 'click':
                movements.append(('mouse', 'click', parts[2], parts[3] == 'True', int(parts[4]), int(parts[5]), float(parts[6])))
            elif parts[1] == 'move':
                movements.append(('mouse', 'move', int(parts[2]), int(parts[3]), float(parts[4])))
            elif parts[1] == 'scroll':
                movements.append(('mouse', 'scroll', int(parts[2]), int(parts[3]), float(parts[4])))
        elif parts[0] == 'keyboard':
            movements.append(('keyboard', parts[1], parts[2], float(parts[3])))

print("The movements are replaying, press \"Backspace\" to stop it")

listener = keyboard.Listener(on_press=on_press)
listener.start()

playback_movements()

listener.join()

print("Replaying finished")
