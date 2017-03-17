from PIL import Image, ImageDraw, ImageFont, ImageChops
from operator import itemgetter

# im1 = Image.open("flashlight1.png")
# im2 = Image.open("flashlight2.png")
# im3 = Image.open("flashlight3.png")
# im4 = Image.open("flashlight4.png")

im1 = Image.open("defect_image.jpg")
im2 = Image.open("gallery_image.jpg")

def hist(image1, image2):
    diff = ImageChops.difference(image1, image2)
    diff.show()
    print diff.histogram()

def check_for_beams(im):
    beams = im.crop((5, 5, 24, 15))
    colors = beams.getcolors()
    return [sum(c[1]) for c in colors]

def compare(im1, im2):
    return sum(im1[1]) - sum(im2[1])

def get_hues(colors):
    text_width = 40
    image_width = 300
    height = 20

    # sorted_colors = sorted(colors, cmp=compare, reverse=True)
    sorted_colors = sorted(colors, key=itemgetter(0), reverse=True)
    w = text_width + image_width
    h = len(sorted_colors) * height
    bg = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(bg)
    for i, c in enumerate(sorted_colors):
        draw.text((text_width*0.1, height*i + height*0.3), str(c[0]), (0, 0, 0))
        im = Image.new("RGB", (image_width, height), c[1])
        bg.paste(im, (text_width, i * height))
    return bg

hist(im1, im2)

# print(check_for_beams(im1))
# print(check_for_beams(im2))

# h = ImageChops.difference(im2, im4).histogram()
# print h

# print(im1.getcolors())
# hues = get_hues(im1.getcolors())
# hues.save("temp1.png")
# hues = get_hues(im2.getcolors())
# hues.save("temp2.png")
# # hues.show()

# print(rmsdiff(im1, im2))
# print(rmsdiff(im1, im3))
# print(rmsdiff(im2, im4))
