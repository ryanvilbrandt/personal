# Inspired by https://blog.confiant.com/confiant-malwarebytes-uncover-steganography-based-ad-payload-that-drops-shlayer-trojan-on-mac-cd31e885c202
# Creates an image file out of a string of characters, with each color (RGB) being a different ASCII character.

from math import ceil
from PIL import Image


def generate_image_size(length):
    """
    Takes a length of a string and finds the best rectangular area to pack it into. Will err towards squares and
    chop off any unused rows at the bottom.
    :param length:
    :return:
    """
    sqrt = length ** 0.5
    width = ceil(sqrt)
    height = ceil(length / width)
    return width, height


def normalize_color(c):
    """
    Takes a character and converts it to a value between 0 and 255.
    :param c:
    :return:
    """
    # scale = (255 - 0) / (122 - 97)
    # return max(min(ceil((ord(c.lower()) - 97) * scale), 255), 0)
    return ord(c)


def string_to_pixels(s):
    """
    Converts a string to a list of RGB tuples. For example, "ABCDE" converts to [(65, 66, 67), (68, 69, 0)]
    Actual values depend on the normalize_colors() function.
    :param s:
    :return:
    """
    pixel_list = []
    pixel = []
    for c in s:
        pixel.append(normalize_color(c))
        if len(pixel) == 3:
            pixel_list.append(tuple(pixel))
            pixel = []
    # Pad any leftover values with 0 to make a whole pixel
    if len(pixel) > 0:
        while len(pixel) < 3:
            pixel.append(0)
        pixel_list.append(tuple(pixel))
    return tuple(pixel_list)


def pixels_to_string(pixel_list):
    """
    Takes a list of 3-tuples of RGB values, and converts them to a string. For example,
    For example, [(65, 66, 67), (68, 69, 0)] converts to "ABCDE\x00"
    :param pixel_list:
    :return:
    """
    out_string = ""
    for p in pixel_list:
        for c in p:
            out_string += chr(c)
    return out_string.strip("\x00")


def main(s, scale=0):
    print("Creating new image")
    size = generate_image_size(ceil(len(s) / 3))
    print(size)
    im = Image.new("RGB", size)
    print("Generating image")
    list_of_pixels = string_to_pixels(s)
    # print(list_of_pixels)
    im.putdata(list_of_pixels)
    print("Showing image")
    if scale > 0:
        im.resize((size[0] * scale, size[1] * scale), resample=0).show()
    else:
        im.show()
    list_of_pixels = list(im.getdata())
    print(repr(pixels_to_string(list_of_pixels)))


main("The quick brown fox jumped over the lazy dog.", 20)
# main("What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated "
#      "top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, "
#      "and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in "
#      "the entire US armed forces. You are nothing to me but just another target. I will wipe you the "
#      "fuck out with precision the likes of which has never been seen before on this Earth, mark my "
#      "fucking words. You think you can get away with saying that shit to me over the Internet? "
#      "Think again, fucker. As we speak I am contacting my secret network of spies across the USA and "
#      "your IP is being traced right now so you better prepare for the storm, maggot. The storm that "
#      "wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be "
#      "anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare "
#      "hands. Not only am I extensively trained in unarmed combat, but I have access to the entire "
#      "arsenal of the United States Marine Corps and I will use it to its full extent to wipe your "
#      "miserable ass off the face of the continent, you little shit. If only you could have known "
#      "what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe "
#      "you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the "
#      "price, you goddamn idiot. I will shit fury all over you and you will drown in it. "
#      "You're fucking dead, kiddo.", 8)