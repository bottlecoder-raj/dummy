#!/usr/bin/env python3
# robotic_eye.py
# Robotic single-eye animation for SSD1306 using luma.oled + PIL

import time
import math
import random
from PIL import Image, ImageDraw

# luma imports (install with: pip3 install luma.oled pillow)
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

# --- Display init (edit if your address/port differ) ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

W, H = device.width, device.height

# Eye geometry
eye_bbox = (14, 2, W - 14, H - 2)  # major oval bounding box (x0,y0,x1,y1)
center_x = (eye_bbox[0] + eye_bbox[2]) // 2
center_y = (eye_bbox[1] + eye_bbox[3]) // 2
eye_width = eye_bbox[2] - eye_bbox[0]
eye_height = eye_bbox[3] - eye_bbox[1]

# animation parameters
fps = 30
frame_delay = 1.0 / fps
scan_speed = 0.06         # angular step per frame for the scanner
pupil_radius = 8
iris_radius = 18
ring_steps = 3            # number of concentric ring outlines
blink_chance_per_second = 0.08  # chance to start a blink each second
blink_duration = 0.09     # closed-eye hold
half_blink_frames = 2

def draw_eye_base(draw):
    """Draw the outer eye shape and concentric ring outlines."""
    # Outer eye (outline)
    draw.ellipse(eye_bbox, outline=255)

    # Concentric rings to simulate 'glow'
    for i in range(1, ring_steps + 1):
        shrink_x = int((eye_width / 2) * (i * 0.12))
        shrink_y = int((eye_height / 2) * (i * 0.12))
        bbox = (
            center_x - (eye_width // 2) + shrink_x,
            center_y - (eye_height // 2) + shrink_y,
            center_x + (eye_width // 2) - shrink_x,
            center_y + (eye_height // 2) - shrink_y,
        )
        draw.ellipse(bbox, outline=255)

def draw_pupil(draw, px, py, radius):
    """Draw the pupil (solid circle)."""
    bbox = (px - radius, py - radius, px + radius, py + radius)
    draw.ellipse(bbox, fill=255)

def draw_iris_marker(draw, angle, length= (iris_radius + 6)):
    """Draw a small radial marker to act as a scanner / indicator."""
    # angle in radians; draw a line from near center outward
    ax = center_x + int(math.cos(angle) * 6)
    ay = center_y + int(math.sin(angle) * 6)
    bx = center_x + int(math.cos(angle) * length)
    by = center_y + int(math.sin(angle) * length)
    draw.line((ax, ay, bx, by), fill=255)

def frame_open(pupil_x, pupil_y, scanner_angle):
    img = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(img)
    draw_eye_base(d)
    # iris small filled ring around pupil (simulated by tiny ellipse outline)
    iris_bbox = (pupil_x - iris_radius, pupil_y - iris_radius, pupil_x + iris_radius, pupil_y + iris_radius)
    d.ellipse(iris_bbox, outline=255)
    # pupil
    draw_pupil(d, pupil_x, pupil_y, pupil_radius)
    # scanner marker
    draw_iris_marker(d, scanner_angle)
    return img

def frame_half_blink():
    img = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(img)
    draw_eye_base(d)
    # half-closed — draw a filled rectangle across upper half of pupil area
    lid_y = center_y + 2
    d.rectangle((eye_bbox[0], lid_y - 6, eye_bbox[2], lid_y + 6), fill=255)
    # optional small pupil hint
    d.ellipse((center_x - 6, center_y - 2, center_x + 6, center_y + 4), fill=255)
    return img

def frame_closed():
    img = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(img)
    draw_eye_base(d)
    # closed eye line
    d.line((eye_bbox[0] + 6, center_y, eye_bbox[2] - 6, center_y), fill=255, width=2)
    return img

def clamp(val, a, b):
    return max(a, min(b, val))

# --- animation main ---
try:
    scanner_angle = 0.0
    pupil_angle = 0.0
    pupil_radius_motion = (eye_width // 2 - iris_radius - 6)  # how far pupil can move from center
    last_time = time.time()
    blink_timer = 0
    in_blink = False
    while True:
        now = time.time()
        dt = now - last_time
        last_time = now

        # scanner rotates steadily
        scanner_angle += scan_speed
        if scanner_angle > math.tau:  # math.tau == 2*pi in Python 3.6+
            scanner_angle -= math.tau

        # pupil makes a mechanical oscillation plus occasional focus shift
        pupil_angle += 0.08  # base oscillation speed
        px = center_x + int(math.cos(pupil_angle * 0.8) * (pupil_radius_motion * 0.6))
        py = center_y + int(math.sin(pupil_angle * 0.5) * (pupil_radius_motion * 0.25))
        px = clamp(px, eye_bbox[0] + pupil_radius + 2, eye_bbox[2] - pupil_radius - 2)
        py = clamp(py, eye_bbox[1] + pupil_radius + 2, eye_bbox[3] - pupil_radius - 2)

        # blinking logic: occasional random blink
        if not in_blink:
            # chance to start blink per frame scaled by dt
            if random.random() < blink_chance_per_second * dt:
                in_blink = True
                # do half-blink frames before closed
                for _ in range(half_blink_frames):
                    device.display(frame_half_blink())
                    time.sleep(frame_delay)
                device.display(frame_closed())
                time.sleep(blink_duration)
                # half-open again
                for _ in range(half_blink_frames):
                    device.display(frame_half_blink())
                    time.sleep(frame_delay)
                in_blink = False
                # small pause after blink
                time.sleep(0.02)
                continue  # continue outer loop to recalc

        # build open-eye frame with scanner + pupil
        img = frame_open(px, py, scanner_angle)
        device.display(img)

        # control framerate roughly
        time.sleep(frame_delay)

except KeyboardInterrupt:
    # Clear display on exit
    try:
        device.clear()
    except Exception:
        pass
    print("\nExiting robotic_eye.py")