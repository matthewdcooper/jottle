import os
import shutil

from markdown import markdown


def make_file(dirpath, filename):
    filepath = os.path.join(dirpath, filename)
    if os.path.exists(filepath):
        raise FileExistsError
    open(filepath, 'a').close()


def make_dir(dirpath, dirname):
    dirpath = os.path.join(dirpath, dirname)
    if os.path.exists(dirpath):
        raise FileExistsError
    os.mkdir(dirpath)


def save(filepath, text):
    with open(filepath, "w") as f:
        f.write(text)

def rename(filepath, new_name):
    parent, _ = os.path.split(filepath)
    new_filepath = os.path.join(parent, new_name)
    print("renaming", filepath, new_filepath)
    os.rename(filepath, new_filepath)



def delete_dir(dirpath):
    shutil.rmtree(dirpath, ignore_errors=True)


def delete_file(filepath):
    os.remove(filepath)


def get_html_from_md(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError
    with open(filepath, "r") as f:
        html = markdown(f.read())
    return html


