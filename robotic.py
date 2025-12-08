from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw
import time

# Display setup
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

def draw_eye(draw, x, y, open=True):
    # Eye outline
    draw.ellipse((x, y, x+50, y+50), outline=255, width=2)

    if open:
        # Iris
        draw.ellipse((x+18, y+18, x+32, y+32), fill=255)
    else:
        # Closed eye (straight line)
        draw.line((x, y+25, x+50, y+25), fill=255, width=3)

while True:
    # ---- EYES OPEN ----
    img = Image.new("1", (128, 64), 0)
    draw = ImageDraw.Draw(img)

    draw_eye(draw, 10, 7, open=True)   # Left eye
    draw_eye(draw, 68, 7, open=True)   # Right eye

    device.display(img)
    time.sleep(1.5)

    # ---- BLINK ----
    img = Image.new("1", (128, 64), 0)
    draw = ImageDraw.Draw(img)

    draw_eye(draw, 10, 7, open=False)
    draw_eye(draw, 68, 7, open=False)

    device.display(img)
    time.sleep(0.15)