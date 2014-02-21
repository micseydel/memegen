from datetime import datetime

from bson.objectid import ObjectId

from objects import MemeText

ID = "_id"
template_ID = "template_id"
template = "template"
FILENAME = "filename"
MEME_TEXT = "meme_text"
TITLE = "title"
CREATOR_ID = "creator_id"
CREATION_TIME = "creation_time"


def get_templates(db):
    "returns a list of template records"
    return db.templates.find()


def get_template_filename(db, _id):
    "returns precisely one string as filename, or None if _id not found"
    result = db.templates.find({ID: ObjectId(_id)})
    return result[0][FILENAME] if result else None


def create_template(db, filename, title):
    return db.templates.insert({FILENAME: filename, TITLE: title})


def get_memes(db):
    "get ALL THE MEMES"
    return db.memes.find()


def create_meme(db, template_id, meme_text, creator_id):
    "returns meme id of the meme created in the database"
    meme = {
        template_ID: template_id,
        MEME_TEXT: MemeText("top", "bottom"),
        CREATOR_ID: creator_id,
        CREATION_TIME: datetime.utcnow()
    }

    return db.memes.insert(meme)
