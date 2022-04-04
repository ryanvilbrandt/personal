import ctypes
import os.path
import random
import re
from argparse import Namespace
from glob import glob
from time import sleep

import win32evtlog
import win32evtlogutil

SPI_SETDESKWALLPAPER = 20
DELAY = 60 * 3
ERROR_DELAY = 10
FILE_LIST_PATH = "wallpaper_files.txt"


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Desktop cycler. Reads from a list of files and sets your desktop wallpapers to a random file at a set time period.")
    parser.add_argument("--add-folder", help="Adds all files in the given folder to the file list")
    parser.add_argument("--include-subdirectories", help="When adding files from a folder, include all subdirectories", default=False, action="store_true")
    return parser.parse_args()


def main(args: Namespace):
    if args.add_folder:
        add_folder_to_file_list(folder_path=args.add_folder, include_subdirectories=args.include_subdirectories)
    else:
        run_loop()


def add_folder_to_file_list(file_path: str=None, folder_path: str=None, include_subdirectories=False):
    file_list = set(read_file_list())
    if file_path:
        file_list.add(file_path)
    elif folder_path:
        file_list.update(set(get_file_list(folder_path, include_subdirectories)))
    file_list = sorted(list(file_list))
    with open(FILE_LIST_PATH, "w") as f:
        f.write("\n".join(file_list))


def read_file_list() -> list:
    if not os.path.isfile(FILE_LIST_PATH):
        return []
    with open(FILE_LIST_PATH) as f:
        return re.split(r"\r?\n", f.read())


def get_file_list(folder_path: str, include_subdirectories: bool=False):
    file_list = []
    for path in glob(folder_path + r"\*"):
        if os.path.isdir(path) and include_subdirectories:
            file_list += get_file_list(path, include_subdirectories)
        else:
            file_list.append(path)
    return file_list


def run_loop():
    file_list = read_file_list()
    while True:
        success = set_desktop_wallpaper(random.choice(file_list))
        sleep(DELAY if success else ERROR_DELAY)


def set_desktop_wallpaper(path: str) -> bool:
    path = os.path.abspath(path)
    # Windows doesn't return an error if we set the wallpaper to an invalid path, so do a check here first.
    if not os.path.isfile(path):
        create_windows_event_log(
            "Couldn't find the file {}".format(path),
            event_type=win32evtlog.EVENTLOG_ERROR_TYPE,
            event_id=2
        )
        return False
    create_windows_event_log("Setting wallpaper to {}".format(path))
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    return True


def create_windows_event_log(message, event_type=win32evtlog.EVENTLOG_INFORMATION_TYPE, event_id=0):
    win32evtlogutil.ReportEvent(
        "Python Wallpaper Cycler",
        event_id,
        eventType=event_type,
        strings=[message],
    )


if __name__ == "__main__":
    main(parse_args())
