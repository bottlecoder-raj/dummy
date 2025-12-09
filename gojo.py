from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw
import time

# Initialize OLED
def init_oled():
    serial = i2c(port=1, address=0x3C)
    return ssd1306(serial)

device = init_oled()

image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # -------- Robot Screen Border (rounded rectangle) --------
    draw.rounded_rectangle((5, 5, 122, 59), radius=10, outline=255, width=2)

    # -------- Angry Eyes (Polygon style) --------
    # Left eye (slanted)
    draw.polygon([
        (30, 25),  # left bottom
        (45, 15),  # top right
        (50, 25),  # right bottom
    ], fill=255)

    # Right eye (slanted)
    draw.polygon([
        (78, 15),  # top left
        (93, 25),  # right bottom
        (73, 25),  # left bottom
    ], fill=255)

    # -------- Angry Mouth (sharp polygon shape) --------
    draw.polygon([
        (45, 45),  # left
        (55, 40),  # upper left
        (70, 40),  # upper right
        (80, 45),  # right
        (70, 50),  # bottom right
        (55, 50),  # bottom left
    ], fill=255)

    device.display(image)
sleep(3)