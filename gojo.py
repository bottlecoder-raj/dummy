from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw
import time

# Initialize OLED
def init_oled():
    serial = i2c(port=1, address=0x3C)
    return ssd1306(serial)

device = init_oled()

# Angry Face (Robot Eyes Style)
def angry_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Robot screen outline
    draw.rectangle((10, 10, 118, 54), outline=255, width=2)

    # Slanted triangle eyes (angry)
    draw.polygon([(35, 25), (50, 20), (50, 32)], outline=255, fill=255)
    draw.polygon([(90, 20), (75, 25), (75, 32)], outline=255, fill=255)

    # Angry curved mouth
    draw.arc((45, 32, 85, 60), start=200, end=340, fill=255, width=3)

    device.display(image)

# Happy Face (Robot Eyes Style)
def happy_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)
    draw.arc((40, 30, 85, 55), start=0, end=180, fill=255, width=3)
    device.display(image)

# Neutral Face
def neutral_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)
    draw.line((45, 45, 80, 45), fill=255, width=3)
    device.display(image)

# Sad Face
def sad_face():
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.ellipse((30, 22, 40, 32), outline=255, fill=255)
    draw.ellipse((80, 22, 90, 32), outline=255, fill=255)
    draw.arc((40, 45, 85, 65), start=180, end=360, fill=255, width=3)
    device.display(image)

# Loop through all faces
if __name__ == "__main__":
    while True:
        angry_face()
        time.sleep(1)
        happy_face()
        time.sleep(1)
        neutral_face()
        time.sleep(1)
        sad_face()
        time.sleep(1)
