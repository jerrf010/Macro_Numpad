import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules.macros import Macros, Press, Release, Tap, Delay
from kmk.modules.holdtap import HoldTap

#Initialize the modules
macros = Macros()
holdtap = HoldTap()
rgb = RGB(
    pixel_pin=board.GP21,
    num_pixels=14,
    animation_speed=2,
    refresh_rate=80,
)


# GPIO to key mapping - each line is a new row.
_KEY_CFG = [
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
    board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15,
    board.GP16, board.GP17, board.GP18,
    board.GP19, board.GP20
]

#Macros configuration
F1 = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.R),
    Release(KC.LGUI),
    Delay(100),
    "C:\MacroPadRun\Spotify.lnk",
    Tap(KC.ENTER)
)

F2 = KC.MACRO(
    Press(KC.LCTRL),
    Press(KC.LALT),
    Tap(KC.F11),
    Release(KC.LALT),
    Release(KC.LCTRL),

)

#Define HoldTap keys
RGB_Toggle = KC.HT(F1, KC.RGB_TOG)
RGB_Breath = KC.HT(KC.P1, KC.RGB_MODE_BREATHE)
RGB_Rainbow = KC.HT(KC.P2, KC.RGB_MODE_RAINBOW)
RGB_Breathe_Rainbow = KC.HT(KC.P3, KC.RGB_MODE_BREATHE_RAINBOW)
RGB_Knight = KC.HT(KC.P4, KC.RGB_MODE_KNIGHT)
RGB_Swirl = KC.HT(KC.P0, KC.RGB_MODE_SWIRL)
RGB_Static = KC.HT(KC.P5, KC.RGB_MODE_PLAIN)

# Keyboard implementation class
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = KeysScanner(
            # require argument:
            pins=_KEY_CFG,
            value_when_pressed=False,
            # optional arguments with defaults:
            pull=True,
        )


#Append the modules and extensions to the keyboard instance
keyboard = MyKeyboard()
keyboard.extensions.append(rgb)
keyboard.modules.append(macros)
keyboard.modules.append(holdtap)

# Define the keymap
keyboard.keymap = [
    [
        RGB_Toggle, F2, KC.NO, KC.NO,
        KC.NUMLOCK, KC.PSLS, KC.PAST, KC.PMNS,
        KC.P7, KC.P8, KC.P9, RGB_Knight,
        RGB_Static, KC.P6, KC.PPLS, RGB_Breath,
        RGB_Rainbow, RGB_Breathe_Rainbow, KC.PENT, KC.PDOT,
        RGB_Swirl
    ]    
]

if __name__ == '__main__':
    keyboard.go()