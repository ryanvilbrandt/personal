import os, glob

IGNORE_DIRS = [r"C:\Users\ryan.v\AppData\Local\Android"]

def iterate_directory(dir, target_text):
    """
    Iterates recursively through multiple directories, starting at a given one.
    For each directory, it calls itself and goes deeper.
    For non-directories, it calls the find_text function.
    :param dir: Current working directory
    :param target_text: Text to search for
    :return: True if the target text has been found, False otherwise
    """

    files = glob.glob(os.path.join(dir, "*"))
    for f in files:
        new_path = os.path.join(dir, f)
        print(new_path)
        if new_path in IGNORE_DIRS:
            continue
        if os.path.isdir(f):
            # If the target text was found, end early.
            if iterate_directory(new_path, target_text):
                return True
        else:
            if find_text(new_path, target_text):
                return True
    return False

def find_text(path, target_text):
    try:
        with open(path) as f:
            if target_text in f.read():
                print(f"Text '{target_text}' found in {path}")
                return True
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        pass
    return False

iterate_directory(r"C:\Users\ryan.v", "zyzzywyg")
