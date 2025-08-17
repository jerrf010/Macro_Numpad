import board
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules.macros import Macros, Press, Release, Tap, Delay
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers

# --- Modules ---
macros = Macros()
holdtap = HoldTap()
rgb = RGB(
    pixel_pin=board.GP21,
    num_pixels=14,
    animation_speed=2,
    refresh_rate=80,
)

# --- Idle RGB Config ---
IDLE_TIMEOUT = 20  # seconds before turning RGB off
last_activity_time = time.monotonic()
rgb_on = True

# GPIO to key mapping
_KEY_CFG = [
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
    board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15,
    board.GP16, board.GP17, board.GP18,
    board.GP19, board.GP20
]

# --- Macros ---
F1 = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.R),
    Release(KC.LGUI),
    Delay(100),
    "C:\\MacroPadRun\\Spotify.lnk",
    Tap(KC.ENTER)
)

F2 = KC.MACRO(
    Press(KC.LCTRL),
    Press(KC.LALT),
    Tap(KC.F11),
    Release(KC.LALT),
    Release(KC.LCTRL),
)



# --- Keyboard ---
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()
        self.matrix = KeysScanner(
            pins=_KEY_CFG,
            value_when_pressed=False,
            pull=True,
        )

keyboard = MyKeyboard()
keyboard.extensions.append(rgb)
keyboard.modules.append(macros)
keyboard.modules.append(holdtap)
keyboard.modules.append(Layers())


# --- HoldTap Keys ---
RGB_Toggle = KC.HT(F1, KC.RGB_TOG)

#DEFINE
LAYER_TAP = KC.LT(1, KC.PSLS, prefer_hold=True, tap_interrupted=False, tap_time=200)
# --- Keymap ---
keyboard.keymap = [
    [
        RGB_Toggle, F2, KC.NO, KC.NO,
        KC.NUMLOCK, LAYER_TAP, KC.PAST, KC.PMNS,
        KC.P7, KC.P8, KC.P9, KC.P4,
        KC.P5, KC.P6, KC.PPLS, KC.P1,
        KC.P2, KC.P3, KC.PENT, KC.PDOT,
        KC.P0,
    ],

    [
        RGB_Toggle, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.TRNS, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.RGB_MODE_KNIGHT,
        KC.RGB_MODE_PLAIN, KC.NO, KC.NO, KC.RGB_MODE_BREATHE,
        KC.RGB_MODE_RAINBOW, KC.RGB_MODE_BREATHE_RAINBOW, KC.NO, KC.NO,
        KC.RGB_MODE_SWIRL,
    ]

]

# --- Activity Tracking ---
orig_process_key = keyboard.process_key

def process_key_with_activity(key, is_pressed, int_coord):
    global last_activity_time, rgb_on
    if is_pressed:
        last_activity_time = time.monotonic()
        if rgb_on == False:
            rgb.increase_val(255)
            rgb_on = True
    return orig_process_key(key, is_pressed, int_coord)

keyboard.process_key = process_key_with_activity

# --- Idle Check Hook ---
def idle_rgb_check():
    global rgb_on
    if rgb_on == True and (time.monotonic() - last_activity_time) > IDLE_TIMEOUT:
        rgb.decrease_val(255)
        rgb_on = False

keyboard.before_matrix_scan = idle_rgb_check

# --- Run ---
if __name__ == '__main__':
    keyboard.go()

    