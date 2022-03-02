import ctypes
import os.path
import random
import re
from glob import glob
from time import sleep

SPI_SETDESKWALLPAPER = 20
DELAY = 60 * 3
ERROR_DELAY = 10
FILE_LIST_PATH = "wallpaper_files.txt"


def add_folder_to_file_list(file_path: str=None, folder_path: str=None):
    file_list = set(read_file_list())
    if file_path:
        file_list.add(file_path)
    elif folder_path:
        file_list.update(set(glob(folder_path + r"\*")))
    file_list = sorted(list(file_list))
    with open(FILE_LIST_PATH, "w") as f:
        f.write("\n".join(file_list))


def read_file_list() -> list:
    if not os.path.isfile(FILE_LIST_PATH):
        return []
    with open(FILE_LIST_PATH) as f:
        return re.split(r"\r?\n", f.read())


def set_desktop_wallpaper(path: str) -> bool:
    path = os.path.abspath(path)
    # Windows doesn't return an error if we set the wallpaper to an invalid path, so do a check here first.
    if not os.path.isfile(path):
        print("Couldn't find the file {}".format(path))
        return False
    print("Setting wallpaper to {}".format(path))
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    return True


def run_loop():
    file_list = read_file_list()
    while True:
        success = set_desktop_wallpaper(random.choice(file_list))
        sleep(DELAY if success else ERROR_DELAY)


def main(add_folder: str=None):
    if add_folder:
        add_folder_to_file_list(folder_path=add_folder)
    else:
        run_loop()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Desktop cycler. Reads from a list of files and sets your desktop wallpapers to a random file at a set time period.")
    parser.add_argument("--add-folder", help="Adds all files in the given folder to the file list")
    args = parser.parse_args()
    return args.add_folder


if __name__ == "__main__":
    main(parse_args())
