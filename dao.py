from datetime import datetime

from bson.objectid import ObjectId

from objects import MemeText

ID = "_id"
IMAGE_ID = "image_id"
IMAGE = "image"
FILENAME = "filename"
MEME_TEXT = "meme_text"
TITLE = "title"
CREATOR_ID = "creator_id"
CREATION_TIME = "creation_time"


def get_images(db):
    "returns a list of image records"
    return db.images.find()


def get_image_filename(db, _id):
    "returns precisely one string as filename, or None if _id not found"
    result = db.images.find({ID: ObjectId(_id)})
    return result[0][FILENAME] if result else None


def create_image(db, filename, title):
    return db.images.insert({FILENAME: filename, TITLE: title})


def get_memes(db):
    "get ALL THE MEMES"
    return db.memes.find()


def create_meme(db, image_id, meme_text, creator_id):
    "returns meme id of the meme created in the database"
    meme = {
        IMAGE_ID: image_id,
        MEME_TEXT: MemeText("top", "bottom"),
        CREATOR_ID: creator_id,
        CREATION_TIME: datetime.utcnow()
    }

    return db.memes.insert(meme)
