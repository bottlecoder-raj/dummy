from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw
import time

# Initialize display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

frames = []

# ========== Frame 1: Eye Open ==========
open_eye = Image.new("1", (128, 64), 0)
d = ImageDraw.Draw(open_eye)

# Outer eye
d.ellipse((34, 10, 94, 70), outline=255)  

# Pupil
d.ellipse((58, 32, 70, 44), fill=255)

frames.append(open_eye)

# ========== Frame 2: Half Blink ==========
half = Image.new("1", (128, 64), 0)
d = ImageDraw.Draw(half)

d.rectangle((34, 36, 94, 46), fill=255)  # eyelid

frames.append(half)

# ========== Frame 3: Fully Closed ==========
closed = Image.new("1", (128, 64), 0)
d = ImageDraw.Draw(closed)

d.line((34, 40, 94, 40), fill=255, width=2)

frames.append(closed)

# ========== Animation Loop ==========
while True:
    for f in frames:
        device.display(f)
        time.sleep(0.12)

    # Hold closed eye briefly
    device.display(closed)
    time.sleep(0.15)