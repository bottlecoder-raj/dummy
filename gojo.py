from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
def angry_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Eyes
    draw.line((30, 20, 45, 30), fill=255, width=3)   # Left eye \
    draw.line((45, 20, 30, 30), fill=255, width=3)   # Left eye /
    draw.line((80, 20, 65, 30), fill=255, width=3)   # Right eye /
    draw.line((65, 20, 80, 30), fill=255, width=3)   # Right eye \

    # Angry mouth
    draw.line((40, 45, 85, 45), fill=255, width=3)

    device.display(image)
def happy_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Eyes
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)

    # Smile
    draw.arc((40, 30, 85, 55), start=0, end=180, fill=255, width=3)

    device.display(image)
def neutral_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Eyes
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)

    # Straight mouth
    draw.line((45, 45, 80, 45), fill=255, width=3)

    device.display(image)
def sad_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Eyes
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)

    # Sad mouth
    draw.arc((40, 45, 85, 65), start=180, end=360, fill=255, width=3)

    device.display(image)
import time

while True:
    angry_face()
    time.sleep(1)

    happy_face()
    time.sleep(1)

    neutral_face()
    time.sleep(1)

    sad_face()
    time.sleep(1)