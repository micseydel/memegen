import os

from flask import Flask, request, redirect, url_for, render_template
from flask.ext.pymongo import PyMongo

import dao
import memegenerator
from memetext import MemeText, Transform

app = Flask(__name__)
app.config.from_object(__name__)
mongo = PyMongo(app)
with app.app_context():
    mongo.db.add_son_manipulator(Transform())


@app.route("/")
def index():
    return redirect(url_for("get_images"))


@app.route("/image", methods=["GET"])
def get_images():
    images = []
    for image in dao.get_images(mongo.db):
        id_url = url_for("get_image", _id=image["_id"])
        img_url = url_for("static", filename="images/%s" % image["filename"])
        images.append({"id_url": id_url, "img_url": img_url})

    form_data = {"images": images, "to_upload": True}
    return render_template("grid.html", form_data=form_data)


@app.route("/image/<_id>", methods=["GET"])
def get_image(_id):
    image = {"id": _id, "name": dao.get_image_filename(mongo.db, _id)}
    return render_template("make_meme.html", image=image)


@app.route("/image", methods=["POST"])
def post_images():
    img = request.files["image"]
    img.save("static/images/" + img.filename)

    title = os.path.splitext(img.filename)[0]
    img_id = dao.create_image(mongo.db, img.filename, title)

    return redirect(url_for("get_image", _id=img_id))


@app.route("/meme", methods=["GET"])
def get_memes():
    images = []
    for image in dao.get_memes(mongo.db):
        path = "memes/%s.png" % image["_id"]
        img_url = id_url = url_for("static", filename=path)
        images.append({"img_url": img_url, "id_url": id_url})

    form_data = {"images": images, "to_upload": False}
    return render_template("grid.html", form_data=form_data)


@app.route("/meme", methods=["POST"])
def post_meme():
    image_id = request.form["image"]
    top = request.form["top"]
    bottom = request.form["bottom"]

    meme_id = dao.create_meme(mongo.db, image_id, MemeText(top, bottom), None)

    image_name = dao.get_image_filename(mongo.db, image_id)
    memegenerator.gen_meme(image_name, top, bottom, meme_id)

    return redirect(url_for("static", filename="memes/%s.png" % meme_id))


def main():
    import sys
    if "-d" in sys.argv or "--debug" in sys.argv:
        print "Running in debug mode"
        app.debug = True
    print "Server is available externally"
    app.run("0.0.0.0")


if __name__ == "__main__":
    main()
