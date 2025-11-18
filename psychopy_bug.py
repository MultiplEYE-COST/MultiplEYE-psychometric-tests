from psychopy.hardware import keyboard
from psychopy import core, gui
from psychopy import visual


win = visual.Window()
test_text = visual.TextStim(win, text='test')
test_text.draw()
win.flip()
experiment_keyboard = keyboard.Keyboard()

# ask for keys for 10 seconds
ms = 10000
time_left = core.getTime() + ms / 1000.0

all_keys = []

while core.getTime() < time_left:
    keys = experiment_keyboard.getKeys(keyList=None, clear=True, waitRelease=False)
    if any(key.name[0] == 'escape' for key in keys):
        print('Found esc key!!')

    # Get only keys from the key_list
    if experiment_keyboard.getKeys(keyList=['escape', 'space', 'a', 'm', 'n'], clear=False, waitRelease=False):
        print('Found key from key_list!!')

    all_keys.extend(keys)


print('found keys:', all_keys)
win.close()