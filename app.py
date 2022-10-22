import sys

from flask import Flask, render_template, url_for, request, redirect
from urllib.parse import unquote
import os
from random import shuffle

app = Flask(__name__)

IMAGE_SUFFIX = {"jpg", "png", "jpeg", "bmp", "gif"}


def filter_images(file_list):
    images_list = [image for image in file_list if image.split(".")[-1].lower() in IMAGE_SUFFIX]
    images_list.sort()
    return images_list


image_dir = "static/images"
images = [image for image in filter_images(os.listdir(image_dir))]

album_dir = "static/albums"
album_list = os.listdir(album_dir)
album_dict = {}
for album in album_list:
    album_images = [image for image in filter_images(os.listdir(os.path.join(album_dir, album)))]

    album_dict[album] = [os.path.join(album_dir, album, image) for image in album_images]
# album_dict[album] = os.listdir(os.path.join(album_dir, album))

album_pics = list(album_dict.values())
album_titles = list(album_dict.keys())

print(str(len(images)) + " images loaded")
print(str(len(album_list)) + " albums loaded")


######## ROUTES ###########
@app.route("/")
def index():
    return redirect(url_for("carousel"))


@app.route("/carousel")
def carousel():
    shuffle(images)
    return render_template("carousel.html", images=images)


@app.route("/albums")
def albums():
    return render_template("albums.html", album_pics=album_pics, album_titles=album_titles)


@app.route("/albums/<album>")
def view_album(album):
    album = unquote(album)  # to remove those %20 formatting since urls cannot have spaces/etc.
    current_album_path = os.path.join(album_dir, album)
    current_album_pics = filter_images(os.listdir(current_album_path))
    return render_template("album_viewer.html", current_album_pics=current_album_pics, current_album_title=album)


if __name__ == "__main__":
    app.run()
