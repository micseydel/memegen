import os
from datetime import datetime

from pymongo import MongoClient

from objects import MemeText, Transform

TEMPLATES_LOCATION = "static/templates"
MEMES_LOCATION = "static/memes"

client = MongoClient()
db = client.injokes
db.add_son_manipulator(Transform())

# collections
templates = db.templates
memes = db.memes
users = db.users

templates.remove()  # wipe existing database
for filename in os.listdir(TEMPLATES_LOCATION):
    template = {
        "filename": filename,
        "title": os.path.splitext(filename)[0],
    }

    templates.insert(template)

memes.remove()
for filename in os.listdir(MEMES_LOCATION):
    meme = {
        "filename": filename,
        "_id": os.path.splitext(filename)[0],
        "meme_text": MemeText("top", "bottom"),
        "creator_id": 0,
        "creation_time": datetime.utcnow()
    }

    memes.insert(meme)

users.remove()
users.insert({"name": "michael"})
