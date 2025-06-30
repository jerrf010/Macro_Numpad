import storage
# Disable USB drive to prevent CircuitPython from mounting as a storage device
storage.disable_usb_drive()
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

import board
import digitalio
import time
import random
import math
import usb_hid
import neopixel

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# --- Configuration ---
NUM_LEDS = 14  # Number of NeoPixel LEDs
leds = neopixel.NeoPixel(board.GP21, NUM_LEDS, brightness=1.0, auto_write=False)
NUM_EFFECTS = 30  # Number of lighting effects
slash_index = 5  # Index for the slash key
enter_index = 18  # Index for the enter key
slash_timeout = 0.2  # Time to wait for slash key combo (in seconds)
suppress_combo_keys = False  # Suppress combo key actions

# --- State ---
buttons = []  # List to hold button objects
states = []   # List to track button states (True = released, False = pressed)
# Define button pins and their corresponding actions
for pin, _ in [
    (board.GP0, "SPOTIFY"), (board.GP1, Keycode.F2), (board.GP2, Keycode.F3),
    (board.GP3, Keycode.F4), (board.GP4, Keycode.KEYPAD_NUMLOCK), (board.GP5, Keycode.KEYPAD_FORWARD_SLASH),
    (board.GP6, Keycode.KEYPAD_ASTERISK), (board.GP7, Keycode.KEYPAD_MINUS), (board.GP8, Keycode.KEYPAD_SEVEN),
    (board.GP9, Keycode.KEYPAD_EIGHT), (board.GP10, Keycode.KEYPAD_NINE), (board.GP11, Keycode.KEYPAD_FOUR),
    (board.GP12, Keycode.KEYPAD_FIVE), (board.GP13, Keycode.KEYPAD_SIX), (board.GP14, Keycode.KEYPAD_PLUS),
    (board.GP15, Keycode.KEYPAD_ONE), (board.GP16, Keycode.KEYPAD_TWO), (board.GP17, Keycode.KEYPAD_THREE),
    (board.GP18, Keycode.KEYPAD_ENTER), (board.GP19, Keycode.KEYPAD_PERIOD), (board.GP20, Keycode.KEYPAD_ZERO),
]:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)
    states.append(True)

# List of actions for each button
actions = [
    "SPOTIFY", Keycode.F2, Keycode.F3, Keycode.F4, Keycode.KEYPAD_NUMLOCK,
    Keycode.KEYPAD_FORWARD_SLASH, Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_MINUS,
    Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_EIGHT, Keycode.KEYPAD_NINE,
    Keycode.KEYPAD_FOUR, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_SIX,
    Keycode.KEYPAD_PLUS, Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO,
    Keycode.KEYPAD_THREE, Keycode.KEYPAD_ENTER, Keycode.KEYPAD_PERIOD,
    Keycode.KEYPAD_ZERO
]

# --- Variables ---
effect_mode = 0  # Current lighting effect
step = 0  # Step counter for animations
sparkle = [0] * NUM_LEDS  # Sparkle intensity for each LED
held_keys = set()  # Currently held keys
slash_timer = None  # Timer for slash key combos
suppress_slash = False  # Suppress slash key action
flash_active = False  # Flash effect active flag
flash_end = 0  # Time when flash effect ends
key_press_time = 0  # Time when a key was pressed
slash_sent = False  # Slash key was sent
effect_file = "/effect_mode.txt"  # File to save effect mode
last_activity = time.monotonic()  # Last activity timestamp
inactive_timeout = 10  # Timeout for inactivity (in seconds)
prev_effect = None  # Previous effect mode for restoration

# --- Helpers ---
def wheel(pos):
    # Generate rainbow colors across 0-255 positions
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def save_effect_mode(mode):
    try:
        with open(effect_file, "w") as f:
            f.write(str(mode))  # Write the mode as a string
    except OSError as e:
        print("Failed to save effect mode:", e)

def load_effect_mode():
    try:
        with open(effect_file, "r") as f:
            return int(f.read().strip())  # Read the mode as an integer
    except (OSError, ValueError):
        return 0  # Default to 0 if file doesn't exist or is invalid

# Load the previous effect mode at startup
previous_effect_mode = load_effect_mode()
effect_mode = previous_effect_mode

def boot_up_sequence(duration=5):
    global previous_effect_mode
    global effect_mode
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        for step in range(256):  # Cycle through 256 colors
            for p in range(NUM_LEDS):
                idx = (p * 256 // NUM_LEDS + step) & 255
                leds[p] = wheel(idx)
            leds.show()
            time.sleep(0.01)  # Adjust for speed of the effect
    # Restore previous effect after boot
    effect_mode = load_effect_mode()

def launch_spotify():
    # Launch Spotify using Windows Run dialog
    kbd.press(Keycode.WINDOWS, Keycode.R)
    kbd.release_all()
    time.sleep(0.2)
    layout.write('"C:\\MacroPadRun\\Spotify.lnk"')
    time.sleep(0.1)
    kbd.press(Keycode.ENTER)
    kbd.release(Keycode.ENTER)

# Add a special action for F2
def press_f2_combination():
    kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.F11)
    kbd.release_all()


def trigger_flash(dur=0.1):
    # Trigger a white flash effect for the specified duration
    global flash_active, flash_end
    flash_active = True
    flash_end = time.monotonic() + dur
    leds.fill((255, 255, 255))
    leds.show()

def update_effect():
    # Update the LED effect based on the current mode and step
    global step, sparkle
    step += 1

    # Show gray if flash is active or a key is held
    if flash_active or held_keys:
        leds.fill((128, 128, 128))
        leds.show()
        return

    i = effect_mode % NUM_EFFECTS  # Select effect based on mode

    # --- Lighting Effects ---
    if i == 0:
        # All LEDs off (blank)
        leds.fill((0,0,0))
    elif i == 1:
        # Backlight dimm (white)
        leds.fill((128, 128, 128))
    elif i == 2:
        # Rainbow cycle (smooth)
        for p in range(NUM_LEDS):
            idx = int(p * 256 / NUM_LEDS + step * 2)
            leds[p] = wheel(idx % 255)
    elif i == 3:
        # Smooth color cycling (Red-Green-Blue)
        phase = (step * 0.05) % (3*math.pi)
        r = int((math.sin(phase) + 1) * 127.5)
        g = int((math.sin(phase + 2 * math.pi / 3) + 1) * 127.5)
        b = int((math.sin(phase + 4 * math.pi / 3) + 1) * 127.5)
        leds.fill((r, g, b))
    elif i == 4:
        # White fading strobe
        fade = int((math.sin(step * 0.25) + 1) * 127.5)
        leds.fill((fade, fade, fade))
    elif i == 5:
        # Green moving dot with fading tail
        leds.fill((0, 0, 0))
        for j in range(4):
            pos = (step - j) % NUM_LEDS
            brightness = int(255 * (0.5 ** j))
            leds[pos] = (0, brightness, 0)
    elif i == 6:
        # Blue triple moving dot with fading
        leds.fill((0, 0, 0))
        for j in range(3):
            idx = (step + j) % NUM_LEDS
            brightness = int(255 * (0.7 ** j))
            leds[idx] = (0, 0, brightness)
    elif i == 7:
        # White sparkle with fading
        for p in range(NUM_LEDS):
            if random.random() < 0.07:
                sparkle[p] = 255
            else:
                sparkle[p] = max(0, sparkle[p] - 15)
            leds[p] = (sparkle[p], sparkle[p], sparkle[p])
    elif i == 8:
        # Blue sine wave (fading)
        for p in range(NUM_LEDS):
            angle = (p * 15 + step * 4) % 360
            val = int((math.sin(math.radians(angle)) + 1) * 110)
            leds[p] = (0, 0, val)
    elif i == 9:
        # Rainbow fill fade
        color = wheel((step*2)%255)
        leds.fill(color)
    elif i == 10:
        # Red dot bounce with fading
        leds.fill((0,0,0))
        bounce = abs((step % (2*NUM_LEDS-2)) - (NUM_LEDS-1))
        for j in range(4):
            pos = bounce - j
            if 0 <= pos < NUM_LEDS:
                brightness = int(255 * (0.5 ** j))
                leds[pos] = (brightness, 0, 0)
    elif i == 11:
        # Comet tail (cyan, fading)
        leds.fill((0,0,0))
        for j in range(5):
            idx = (step-j)%NUM_LEDS
            fade = int(255 * (0.8 ** j))
            leds[idx] = (0,fade,fade)
    elif i == 12:
        # Two color ping-pong with fading
        leds.fill((0,0,0))
        pos1 = step%NUM_LEDS
        pos2 = (NUM_LEDS-1-step%NUM_LEDS)
        leds[pos1] = (255,0,255)
        leds[pos2] = (255,255,0)
        if pos1 != pos2:
            leds[(pos1+1)%NUM_LEDS] = (127,0,127)
            leds[(pos2-1)%NUM_LEDS] = (127,127,0)
    elif i == 13:
        # Color wipe (red to green, fading)
        for p in range(NUM_LEDS):
            ratio = p / (NUM_LEDS - 1)
            r = int((1 - ratio) * 255)
            g = int(ratio * 255)
            leds[p] = (r, g, 0)
    elif i == 14:
        # Twinkle (random white sparkles fading)
        for p in range(NUM_LEDS):
            if random.random()<0.08:
                sparkle[p]=255
            else:
                sparkle[p]=max(0,sparkle[p]-15)
            leds[p]=(sparkle[p],sparkle[p],sparkle[p])
    elif i == 15:
        # Fire flicker (fading)
        for p in range(NUM_LEDS):
            r = random.randint(128,255)
            g = random.randint(0,80)
            leds[p] = (r,g,0)
    elif i == 16:
        # Gradient sweep (red to blue, fading)
        for p in range(NUM_LEDS):
            ratio = p/(NUM_LEDS-1)
            val = int((math.sin(step*0.08 + ratio*math.pi)+1)*128)
            leds[p] = (val,0,255-val)
    elif i == 17:
        # Snake (green, fading)
        leds.fill((0,0,0))
        tail = 4
        for j in range(tail):
            leds[(step-j)%NUM_LEDS]=(0,int(255*(0.7**j)),0)
    elif i == 18:
        # Rainbow chase (fading)
        for p in range(NUM_LEDS):
            fade = int((math.sin((step+p)*0.2)+1)*100)
            leds[p] = wheel((p*16 + step*8)%255)
            leds[p] = tuple(int(c*fade/255) for c in leds[p])
    elif i == 19:
        # Color pulse (purple, fading)
        val = int((math.sin(step*0.1)+1)*120)
        leds.fill((val,0,val))
    elif i == 20:
        # 2-color alternate fade
        color1 = (0,255,255)
        color2 = (255,0,255)
        fade = int((math.sin(step*0.15)+1)*127.5)
        leds.fill(tuple(int(a*(255-fade)/255+b*fade/255) for a,b in zip(color1,color2)))
    elif i == 21:
        # Split-wipe (red/blue, fading edge)
        for p in range(NUM_LEDS):
            if p < (step%NUM_LEDS):
                leds[p] = (255,0,0)
            elif p == (step%NUM_LEDS):
                fade = int((math.sin(step*0.5)+1)*127.5)
                leds[p] = (fade,0,255-fade)
            else:
                leds[p] = (0,0,255)
    elif i == 22:
        # Rotating bar (yellow, fading)
        leds.fill((0,0,0))
        for j in range(3):
            idx = (step+j)%NUM_LEDS
            fade = int(255*(0.8**j))
            leds[idx] = (fade,fade//2,0)
    elif i == 23:
        # Meteor shower (white, fading)
        leds.fill((0,0,0))
        for j in range(4):
            idx = (step-j*2)%NUM_LEDS
            fade = int(255 * (0.7 ** j))
            leds[idx] = (fade,fade,fade)
    elif i == 24:
        # Larson scanner (red, fading)
        pos = step % (2*NUM_LEDS-2)
        if pos >= NUM_LEDS:
            pos = 2*NUM_LEDS-2 - pos
        leds.fill((0,0,0))
        for offset in range(-2,3):
            i2 = pos+offset
            if 0<=i2<NUM_LEDS:
                fade = int(255*(0.7**abs(offset)))
                leds[i2] = (fade,0,0)
    elif i == 25:
        # Single LED random color, fading out
        leds.fill((0,0,0))
        idx = step%NUM_LEDS
        fade = int((math.sin(step*0.3)+1)*127.5)
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        leds[idx] = tuple(int(c*fade/255) for c in color)
    elif i == 26:
        # Alternating colors, fading between
        colorA = (255,255,0)
        colorB = (0,128,255)
        fade = int((math.sin(step*0.2)+1)*127.5)
        for p in range(NUM_LEDS):
            base = colorA if (p+step)%2==0 else colorB
            target = colorB if (p+step)%2==0 else colorA
            leds[p] = tuple(int(a*(255-fade)/255+b*fade/255) for a,b in zip(base,target))
    elif i == 27:
        # Rolling fade (purple-blue)
        for p in range(NUM_LEDS):
            val = int((math.sin((step+p)*0.15)+1)*100)
            leds[p] = (val,0,255-val)
    elif i == 28:
        # Police lights (fading flash)
        fade = int((math.sin(step*0.3)+1)*127.5)
        for p in range(NUM_LEDS):
            if p < NUM_LEDS//2:
                leds[p] = (fade,0,0)
            else:
                leds[p] = (0,0,fade)
    elif i == 29:
        # Christmas alternate (green/red, fading)
        fade = int((math.sin(step*0.2)+1)*127.5)
        for p in range(NUM_LEDS):
            base = (0,fade,0) if (p+step)%2==0 else (fade,0,0)
            leds[p] = base

    leds.show()

# --- Main Loop ---
leds.fill((0, 0, 0))
leds.show()

# Boot up sequence
boot_up_sequence(2)

# --- Main Loop ---
held_keys = set()  # Make sure you've defined this above

while True:
    now = time.monotonic()

    # End flash effect if time expired
    if flash_active and now >= flash_end:
        flash_active = False

    # Inactivity reset to default effect
    if now - last_activity >= inactive_timeout:
        if effect_mode != 0:
            prev_effect = effect_mode
            effect_mode = 0
            save_effect_mode(effect_mode)
            update_effect()

    for i, button in enumerate(buttons):
        pressed = not button.value
        action = actions[i]

        # Button just pressed
        if pressed and states[i]:
            last_activity = now
            states[i] = False

            # Handle effect restore
            if effect_mode == 0 and prev_effect is not None:
                effect_mode = prev_effect
                save_effect_mode(effect_mode)
                update_effect()
                prev_effect = None

            if i == slash_index:
                slash_timer = now
                suppress_slash = False
                continue

            elif slash_timer and i == enter_index:
                previous_effect = effect_mode
                effect_mode = (effect_mode + 1) % NUM_EFFECTS
                save_effect_mode(effect_mode)
                step = 0
                sparkle = [0] * NUM_LEDS
                suppress_slash = True
                slash_timer = None
                kbd.release(Keycode.KEYPAD_FORWARD_SLASH)
                kbd.release(Keycode.KEYPAD_ENTER)
                held_keys.discard(Keycode.KEYPAD_FORWARD_SLASH)
                held_keys.discard(Keycode.KEYPAD_ENTER)
                continue

            elif slash_timer and i == 20:  # 0 key combo
                previous_effect = effect_mode
                effect_mode = 0
                save_effect_mode(effect_mode)
                step = 0
                sparkle = [0] * NUM_LEDS
                suppress_slash = True
                slash_timer = None
                kbd.release(Keycode.KEYPAD_FORWARD_SLASH)
                kbd.release(Keycode.KEYPAD_ZERO)
                held_keys.discard(Keycode.KEYPAD_FORWARD_SLASH)
                held_keys.discard(Keycode.KEYPAD_ZERO)
                continue

            # F2 combo key
            if i == 1:
                trigger_flash()
                press_f2_combination()
                continue

            # "SPOTIFY" launcher
            if action == "SPOTIFY":
                trigger_flash()
                launch_spotify()
                continue

            # All other key presses
            trigger_flash()
            if isinstance(action, int) and action not in held_keys:
                kbd.press(action)
                held_keys.add(action)

        # Button just released
        elif not pressed and not states[i]:
            if action in held_keys:
                kbd.release(action)
                held_keys.remove(action)
            states[i] = True

    # Slash timeout handling
    if slash_timer and (now - slash_timer > slash_timeout):
        if not suppress_slash:
            kbd.press(Keycode.KEYPAD_FORWARD_SLASH)
            kbd.release(Keycode.KEYPAD_FORWARD_SLASH)
            held_keys.discard(Keycode.KEYPAD_FORWARD_SLASH)
        slash_timer = None
        suppress_slash = False

    # Emergency release if no buttons held
    if all(b.value for b in buttons) and held_keys:
        for key in list(held_keys):
            kbd.release(key)
        held_keys.clear()

    update_effect()
    time.sleep(0.001)
