import time, random, math
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

# --- Display Setup ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Eye parameters
EYE_SIZE = 46
PUPIL_SIZE = 14
GAP = 8     # space between eyes
LEFT_X = 6  # left eye X
RIGHT_X = LEFT_X + EYE_SIZE + GAP
Y_POS = 9

def draw_eye(draw, x, y, pupil_offset, blink_ratio):
    # Outer eye circle
    draw.ellipse((x, y, x+EYE_SIZE, y+EYE_SIZE), outline=255, width=2)

    # Blinking: scale vertically
    if blink_ratio < 1:
        lid = int((1 - blink_ratio) * (EYE_SIZE // 2))
        draw.rectangle((x, y, x+EYE_SIZE, y+lid), fill=0)
        draw.rectangle((x, y+EYE_SIZE-lid, x+EYE_SIZE, y+EYE_SIZE), fill=0)

    if blink_ratio > 0.2:   # hide pupil when almost closed
        px = x + EYE_SIZE//2 + pupil_offset[0] - PUPIL_SIZE//2
        py = y + EYE_SIZE//2 + pupil_offset[1] - PUPIL_SIZE//2
        draw.ellipse((px, py, px+PUPIL_SIZE, py+PUPIL_SIZE), fill=255)

def random_eye_target():
    # movement radius
    r = 10  
    angle = random.uniform(0, 2*math.pi)
    return (int(r * math.cos(angle)), int(r * math.sin(angle)))

pupil_L = (0,0)
pupil_R = (0,0)
target_L = random_eye_target()
target_R = random_eye_target()

blink_timer = random.uniform(2,5)
blink_state = 1.0
blinking = False

while True:
    dt = 0.05
    time.sleep(dt)

    # ---- PUPIL SMOOTH MOVEMENT ----
    def update_pupil(pos, target):
        px, py = pos
        tx, ty = target
        px += (tx - px) * 0.15
        py += (ty - py) * 0.15
        return (px, py)

    pupil_L = update_pupil(pupil_L, target_L)
    pupil_R = update_pupil(pupil_R, target_R)

    # pick new random target sometimes
    if random.random() < 0.02:
        target_L = random_eye_target()
        target_R = random_eye_target()

    # ---- BLINK LOGIC ----
    blink_timer -= dt
    if blink_timer <= 0 and not blinking:
        blinking = True

    if blinking:
        blink_state -= 0.25
        if blink_state <= 0:
            blink_state = 0
            blinking = "open"

    if blinking == "open":
        blink_state += 0.25
        if blink_state >= 1:
            blink_state = 1
            blinking = False
            blink_timer = random.uniform(2,5)

    # ---- DRAW FRAME ----
    img = Image.new("1", (128,64), 0)
    draw = ImageDraw.Draw(img)

    draw_eye(draw, LEFT_X,  Y_POS, pupil_L, blink_state)
    draw_eye(draw, RIGHT_X, Y_POS, pupil_R, blink_state)

    device.display(img)