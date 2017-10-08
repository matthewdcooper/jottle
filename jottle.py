import os
import hashlib

from collections import namedtuple
from datetime import datetime

from flask import Flask, render_template, request, abort, make_response

import filehelpers as fh
import config


app = Flask(__name__)


def authenticate_password(password):
    hashed = hashlib.sha512(password.encode()).hexdigest()
    return hashed == config.passhash


def authenticate_key(key):
    if not config.passhash:
        return True
    if not key:
        return False
    if key == config.key:
        return True


def browse(path):
    File = namedtuple("File", "path_url name")
    dirs = []
    files = []
    parent, _ = os.path.split(path)

    for name in os.listdir(make_filepath(path)):
        path_url = "/" + os.path.join(path, name)
        f = File(path_url, name)
        if os.path.isdir(make_filepath(f.path_url[1:])):
            dirs.append(f)
        else:
            files.append(f)

    return render_template("browse.html",
                            path=path,
                            parent=parent,
                            dirs=sorted(dirs),
                            files=sorted(files))

def edit(path):
    with open(make_filepath(path), 'r') as f:
        content = f.read()
    return render_template("edit.html",
                            content=content,
                            path=path)


def find_extension(path):
    i = path.rfind(".")
    return path[i:]


def make_filepath(path):
    return os.path.join(config.root, path)


def view(path):
    if find_extension(path) == ".md":
        content = fh.get_html_from_md(make_filepath(path))
    else:
        with open(make_filepath(path), 'r') as f:
            content = "<pre><code>{}</code></pre>".format(f.read())
    parent_url, filename = os.path.split(path)
    parent_url = "/" + parent_url
    file_url = "/" + path
    return render_template("view.html",
                            content=content,
                            parent_url=parent_url,
                            file_url=file_url)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        if not authenticate_password(request.form['password']):
            return render_template("authenticate.html")
        resp = make_response(render_template("authenticate.html"))
        resp.set_cookie('key', config.key)
        return resp
    return render_template("login.html")


@app.route("/", methods = ["GET", "POST"])
@app.route("/<path:path>", methods = ["GET", "POST"])
def index(path=""):
    key = request.cookies.get('key')
    if not authenticate_key(key):
        return render_template("login.html")

    filepath = make_filepath(path)

    # parse POST request, used for simple file commands
    if request.method == "POST":
        if request.form['command'] == "make_file":
            fh.make_file(filepath, request.form['name'])

        elif request.form['command'] == "make_dir":
            fh.make_dir(filepath, request.form['name'])

        elif request.form['command'] == "rename":
            fh.rename(filepath, request.form['new_name'])

        elif request.form['command'] == "save":
            fh.save(filepath, request.form['text'])

        elif request.form['command'] == "delete_dir":
            fh.delete_dir(filepath)

        elif request.form['command'] == "delete_file":
            fh.delete_file(filepath)

        else:
            return "could not understand POST request"
        return "done"

    # if directory then browse
    if os.path.isdir(filepath):
        return browse(path)

    # if not a directory and not a file then 404
    if not os.path.isfile(filepath):
        abort(404)

    # edit
    if "edit" in request.args:
        return edit(path)

    # view
    return view(path)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)

