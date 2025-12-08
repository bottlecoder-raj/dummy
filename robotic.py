#!/usr/bin/env python3
# RoboEyes for Raspberry Pi (SSD1306 128x64)

import time
import numpy as np
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

# --- Display init ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# --- Eye shapes (inspired by FluxGarage RoboEyes) ---
# Basic glowing rectangular robotic eye shapes
normal_eye = [
    "0011111100",
    "0111111110",
    "1111111111",
    "1111111111",
    "1111111111",
    "0111111110",
    "0011111100",
]

blink_eye = [
    "0000000000",
    "0000000000",
    "1111111111",
    "1111111111",
    "0000000000",
    "0000000000",
    "0000000000",
]

# Convert 1/0 strings to numpy
def shape_to_np(shape):
    arr = []
    for row in shape:
        arr.append([1 if c == "1" else 0 for c in row])
    return np.array(arr)

eye_open = shape_to_np(normal_eye)
eye_blink = shape_to_np(blink_eye)

def draw_eye(x, y, shape, scale=4):
    """Draw eye shape at x,y with scaling."""
    h, w = shape.shape
    img = Image.new("1", (128, 64), 0)
    d = ImageDraw.Draw(img)

    for i in range(h):
        for j in range(w):
            if shape[i][j] == 1:
                # draw a scaled block
                d.rectangle(
                    (
                        x + j * scale,
                        y + i * scale,
                        x + (j+1) * scale - 1,
                        y + (i+1) * scale - 1,
                    ),
                    fill=1
                )

    return img


print("Running RoboEyes Pi… Press Ctrl+C to exit.")

try:
    state = 0
    blink_timer = 0

    while True:
        if blink_timer == 0 and np.random.random() < 0.01:
            blink_timer = 4

        if blink_timer > 0:
            img = draw_eye(44, 20, eye_blink)
            blink_timer -= 1
        else:
            img = draw_eye(44, 20, eye_open)

        device.display(img)

        time.sleep(0.07)

except KeyboardInterrupt:
    device.clear()
    print("Stopped.")