import os
import json
from datetime import datetime

from pymongo import MongoClient

from objects import MemeText, Transform

TEMPLATES_LOCATION = "static/templates"
MEMES_LOCATION = "static/memes"
TEMPLATE_DEFAULTS = "template_defaults.json"

FILENAME = "filename"

client = MongoClient()
db = client.injokes
db.add_son_manipulator(Transform())

# collections
templates = db.templates
memes = db.memes
users = db.users

with open(TEMPLATE_DEFAULTS) as template_defaults_f:
    template_defaults = json.load(template_defaults_f)

templates.remove()  # wipe existing database
for filename in os.listdir(TEMPLATES_LOCATION):
    template = template_defaults.get(filename, {})
    template[FILENAME] = filename
    templates.insert(template)

memes.remove()
for filename in os.listdir(MEMES_LOCATION):
    meme = {
        FILENAME: filename,
        "_id": os.path.splitext(filename)[0],
        "meme_text": MemeText("top", "bottom"),
        "creator_id": 0,
        "creation_time": datetime.utcnow()
    }

    memes.insert(meme)

users.remove()
users.insert({"name": "michael"})
