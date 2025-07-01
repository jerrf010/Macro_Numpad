# RGB MacroPad / Numpad

This project is based on the excellent [21 Key Mechanical Numpad by serohs7MakerWorld](https://makerworld.com/en/models/847093-21-key-mechanical-numpad#profileId-794356).

- **List of materials:** [Google Sheets Materials List](https://docs.google.com/spreadsheets/d/1POHebsY6CT1eLJ3NvEvcW8S9I_YbqTaPaNE3qmyI9Bc/edit?gid=1819894683#gid=1819894683)

---

## 📸 Images

![IMG_4481](https://pfst.cf2.poecdn.net/base/image/bddf66d767e515e33839d83b362fbf664346d2a9b74b6b21eec03bfb0b674a9c?w=4032&h=3024&pmaid=410758589)
![IMG_4477](https://pfst.cf2.poecdn.net/base/image/01760af90040a02c106ec97ace9758b6193c2c3e74fcd92d154a3b7d2cddbe10?w=4032&h=3024&pmaid=410758590)
![RGB MacroPad powered on](https://pfst.cf2.poecdn.net/base/image/bddf66d767e515e33839d83b362fbf664346d2a9b74b6b21eec03bfb0b674a9c?w=4032&h=3024&pmaid=410758589)
![RGB MacroPad off](https://pfst.cf2.poecdn.net/base/image/01760af90040a02c106ec97ace9758b6193c2c3e74fcd92d154a3b7d2cddbe10?w=4032&h=3024&pmaid=410758590)

---

## 🎛️ Features

- **21 Programmable Keys:**  
  Assign any key, HID code, or custom shortcut (including app launch).
- **14 NeoPixel LEDs:**  
  30 built-in lighting animations — rainbow, sparkles, comets, fire, police, Christmas, more.
- **Combo Key Actions:**  
  Press `/ + Enter` to cycle lighting effects.  
  Press `/ + 0` to reset effect to default.
- **Persistent Modes:**  
  Saves/restores your last lighting effect, reverts to default after inactivity.
- **Reactive Lighting:**  
  Keypresses trigger a visual flash.
- **Productivity Boost:**  
  One key launches Spotify (customizable), F2 sends Ctrl+Alt+F11, and more.
- **100% Customizable:**  
  All key actions and lighting effects are editable in Python.

---

## 🖥️ Key Mapping

| Pin         | Key Function         |
|-------------|---------------------|
| GP0         | Launch Spotify      |
| GP1         | F2 (with combo)     |
| GP2, GP3    | F3, F4              |
| GP4         | NumLock             |
| GP5         | Keypad `/`          |
| GP6         | Keypad `*`          |
| GP7         | Keypad `-`          |
| GP8-GP10    | Keypad 7, 8, 9      |
| GP11-GP13   | Keypad 4, 5, 6      |
| GP14        | Keypad `+`          |
| GP15-GP17   | Keypad 1, 2, 3      |
| GP18        | Keypad `Enter`      |
| GP19        | Keypad `.`          |
| GP20        | Keypad 0            |

> *Easy to remap — just change the `actions` list in the code!*

---

## 🌈 Lighting Effects

**30 built-in modes, including:**
- Blank/off, dim backlight
- Rainbow cycle
- RGB color cycling
- Pulsing, strobe, sine waves
- Sparkles, comets, fire flicker
- Police lights, Christmas, and more!

**Switch effects:** Press `/ + Enter`  
**Return to default:** After 10s inactivity or `/ + 0`

---

## 🚀 Quick Start

1. **Wire up:**  
   - 21 momentary switches to GP0–GP20  
   - NeoPixel DIN to GP21 (default, can change in code)
2. **Install CircuitPython**  
   - Copy this code and needed libraries (`adafruit_hid`, `neopixel`) to your board.
3. **Plug in:**  
   - Connect via USB. It works as a HID keyboard!
4. **Enjoy:**  
   - Press keys, launch apps, and enjoy animated lighting.

---

## 🛠️ Customization

- **Change key actions:**  
  Edit the `actions` array in the code.
- **Edit/add lighting effects:**  
  Tweak the `update_effect()` function.
- **Change LED count, pins, or combos:**  
  Adjust `NUM_LEDS`, pin assignments, and combo logic as needed.

---

## ⚡ Example: Launch Spotify

Press the first key (GP0) to instantly launch Spotify via Windows Run (`Win+R`).

---

## 📦 Materials

See the full [Materials List (Google Sheets)](https://docs.google.com/spreadsheets/d/1POHebsY6CT1eLJ3NvEvcW8S9I_YbqTaPaNE3qmyI9Bc/edit?gid=1819894683#gid=1819894683) for sources, quantities, and pricing.

| # | Material | Example Source | Price (USD) | Notes |
|---|----------|---------------|-------------|-------|
| 1 | 3D Printed Case | [MakerWorld Model](https://makerworld.com/en/models/847093-21-key-mechanical-numpad#profileId-794356) | Free | STL/3MF files |
| 2 | Raspberry Pi Pico (non-Wireless, no headers) | Amazon.ca | 13.95 | |
| 3 | GATERON G Pro V3 Switches (3-pin) | AliExpress | 4.35 | 30pcs, G Yellow 3.0 |
| 4 | Number Keypad PBT Keycaps (17 keys, Sunset theme) | AliExpress | 16.37 | 3 Front Printed |
| 5 | M3 x 16mm Flat Head Screws (50 pcs) | AliExpress | 3.90 | |
| 6 | M3 Brass Knurled Heat Inserts (4.5mm OD, 4mm L, 50 pcs) | AliExpress | 2.47 | For 3D case |
| 7 | WS2812B Led Lights DC5V WS2812 RGB Led Strip | AliExpress | 4.86 | |
|   | **Total** | | **45.90** | (Approx., varies by supplier) |

---

## ❤️ Why You'll Love This MacroPad

- **Instant shortcuts:** One-tap commands, combos, and app launches.
- **Stunning visuals:** Dozens of animated RGB modes.
- **Fully hackable:** All Python, easy to extend.
- **Desk personality:** Useful, beautiful, and fun.

---

## 🔗 License

MIT License  
(c) Aiden So

---

**Build, customize, and enjoy a macropad that's as unique as you are!**
