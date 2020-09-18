import os
from math import ceil, floor

from PIL import Image

FILE_PATH = "filter_imei.py"
RESIZE_RATIO = 8

def safe_read(f, bytes):
    # If a read hits the end of the file, returns a null byte instead
    r = f.read(bytes)
    if r in (b'', ''):
        return '\x00'
    return r

file_size = os.stat(FILE_PATH).st_size
print("File size:", file_size)
pixel_count = ceil(file_size / 3)
print("Pixel count:", pixel_count)
width = int(ceil(pixel_count ** 0.5))
height = int(ceil(pixel_count / width))
print("Size:", width, "/", height)

with open(FILE_PATH, 'rb') as f:
    img = Image.new('RGB', (width, height), "white")
    pixels = img.load()

    x, y = 0, 0
    while f.tell() < file_size:
        color = (safe_read(f, 1), safe_read(f, 1), safe_read(f, 1))
        color = tuple(map(ord, color))
        # print(color)
        pixels[x, y] = color
        x += 1
        if x >= width:
            x = 0
            y += 1

    if RESIZE_RATIO != 1:
        img = img.resize((RESIZE_RATIO * width, RESIZE_RATIO * height), Image.NEAREST)
    img.show()
