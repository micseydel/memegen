import os

from flask import Flask, request, redirect, url_for, render_template
from flask.ext.pymongo import PyMongo

import dao
import memegenerator
from objects import MemeText, Transform

app = Flask(__name__)
app.config.from_object(__name__)
mongo = PyMongo(app)
with app.app_context():
    mongo.db.add_son_manipulator(Transform())


@app.route("/")
def home():
    templates = []
    for template in dao.get_templates(mongo.db):
        id_url = url_for("get_template", _id=template["_id"])
        img_url = url_for("static", filename="templates/%s" % template["filename"])
        templates.append({"id_url": id_url, "img_url": img_url})

    form_data = {"templates": templates, "to_upload": True}
    return render_template("home_page.html", form_data=form_data)


@app.route("/template/<_id>", methods=["GET"])
def get_template(_id):
    template = {"id": _id, "name": dao.get_template_filename(mongo.db, _id)}
    return render_template("make_meme.html", template=template)


@app.route("/template", methods=["POST"])
def post_templates():
    img = request.files["template"]
    img.save("static/templates/" + img.filename)

    title = os.path.splitext(img.filename)[0]
    img_id = dao.create_template(mongo.db, img.filename, title)

    return redirect(url_for("get_template", _id=img_id))


@app.route("/memes", methods=["GET"])
def get_memes():
    templates = []
    for template in dao.get_memes(mongo.db):
        path = "memes/%s.png" % template["_id"]
        img_url = id_url = url_for("static", filename=path)
        templates.append({"img_url": img_url, "id_url": id_url})

    form_data = {"templates": reversed(templates), "to_upload": False}
    return render_template("memes.html", form_data=form_data)


@app.route("/post_meme", methods=["POST"])
def post_meme():
    template_id = request.form["template"]
    top = request.form["top"]
    bottom = request.form["bottom"]

    meme_id = dao.create_meme(mongo.db, template_id, MemeText(top, bottom), None)

    template_name = dao.get_template_filename(mongo.db, template_id)
    memegenerator.gen_meme(template_name, top, bottom, meme_id)

    return redirect(url_for("get_memes"))


def main():
    import sys
    if "-d" in sys.argv or "--debug" in sys.argv:
        print "Running in debug mode"
        app.debug = True
    print "Server is available externally"
    app.run("0.0.0.0")


if __name__ == "__main__":
    main()
