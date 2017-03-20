import os
from math import ceil, floor

from PIL import Image

FILE_PATH = "gallery_image.jpg"

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
width = ceil(pixel_count ** 0.5)
height = ceil(pixel_count / width)
print("Size:", width, "/", height)

with open(FILE_PATH, 'rb') as f:
    pixels = img.load()

    x, y = 0, 0
    while f.tell() < file_size:
        color = (safe_read(f, 1), safe_read(f, 1), safe_read(f, 1))
        color = tuple(map(ord, color))
        pixels[x, y] = color
        x += 1
        if x >= width:
            x = 0
            y += 1

    img.show()
