import pynput.mouse as mouse
import pynput.keyboard as keyboard
import time

movements = []

print("Recording is started, to stop it press \"Esc")
print("Wait 5 seconds before the script starts recording (its needed to give you some time to open minecraft and be ready to record your moves)")

time.sleep(5)

print("Recording started")

def on_click(x, y, button, pressed):
    movements.append(('mouse', 'click', button.name, pressed, x, y, time.time()))

def on_move(x, y):
    movements.append(('mouse', 'move', x, y, time.time()))

def on_scroll(x, y, dx, dy):
    movements.append(('mouse', 'scroll', dx, dy, time.time()))

def on_press(key):
    try:
        movements.append(('keyboard', 'press', key.char, time.time()))
    except AttributeError:
        movements.append(('keyboard', 'press', key.name, time.time()))

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    try:
        movements.append(('keyboard', 'release', key.char, time.time()))
    except AttributeError:
        movements.append(('keyboard', 'release', key.name, time.time()))

mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()

with open('movements.txt', 'w') as file:
    for movement in movements:
        file.write(" ".join(map(str, movement)) + "\n")

print("Recording finished and saved to movements.txt")
