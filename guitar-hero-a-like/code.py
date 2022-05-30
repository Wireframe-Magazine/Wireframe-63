import time
import board
import touchio
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

touch_pad_z = board.GP2
touch_z = touchio.TouchIn(touch_pad_z)

touch_pad_x = board.GP3
touch_x = touchio.TouchIn(touch_pad_x)

touch_pad_c = board.GP4
touch_c = touchio.TouchIn(touch_pad_c)

touch_pad_v = board.GP5
touch_v = touchio.TouchIn(touch_pad_v)

touch_pad_b = board.GP6
touch_b = touchio.TouchIn(touch_pad_b)

touchpads = [touch_z, touch_x, touch_c, touch_v, touch_b]
keycodes = [Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B]

thresh_jump = 2500
for pad in touchpads:
    current = pad.raw_value
    pad.threshold = current+thresh_jump

switch = DigitalInOut(board.GP17)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


#need to increase all the sensitivities here as there's quite a bit of cross-talk
#new logic -- if one of the buttons is over the threshold, (say 4000), take the one with the highest value

touch_thresh = 3500
currently_pressed = False
currently_pressed_index = 0

while True:
    
    pressed = False
    max_value = 0
    max_index = 0
    last_key = ""
    for i in range(5):
        value = touchpads[i].raw_value
        if value > touch_thresh:
            pressed = True
        if value > max_value:
            max_value = value
            max_index = i
    if (pressed):
        print(max_index)
        if (not currently_pressed) or currently_pressed_index != max_index:
            keyboard.release(keycodes[currently_pressed_index])
            keyboard.press(keycodes[max_index])
            currently_pressed = True
            currently_pressed_index = max_index

    if (not pressed) and currently_pressed:
        keyboard.release(keycodes[currently_pressed_index])
        currently_pressed = False
    
    #print(touch_b.raw_value)
    
    time.sleep(0.05)
    if not switch.value:
        keyboard.press(Keycode.SPACE)
    else:
        keyboard.release(Keycode.SPACE)