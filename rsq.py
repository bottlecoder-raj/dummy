from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

# Setup display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Create blank image
img = Image.new("1", (128, 64), 0)
draw = ImageDraw.Draw(img)

# Draw rounded rectangle
draw.rounded_rectangle((10, 10, 60, 60), radius=12, outline=255, width=2)

# Display it
device.display(img)