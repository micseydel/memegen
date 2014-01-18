import os
from datetime import datetime

from pymongo import MongoClient

from memetext import MemeText, Transform

TEMPLATES_LOCATION = "static/images"
MEMES_LOCATION = "static/memes"

client = MongoClient()
db = client.injokes
db.add_son_manipulator(Transform())

# collections
images = db.images
memes = db.memes
users = db.users

images.remove()  # wipe existing database
for filename in os.listdir(TEMPLATES_LOCATION):
    image = {
        "filename": filename,
        "title": os.path.splitext(filename)[0],
    }

    images.insert(image)

memes.remove()
for filename in os.listdir(MEMES_LOCATION):
    meme = {
        "filename": filename,
        "title": os.path.splitext(filename)[0],
        "meme_text": MemeText("top", "bottom"),
        "creator_id": 0,
        "creation_time": datetime.utcnow()
    }

    memes.insert(meme)

users.remove()
users.insert({"name": "michael"})
