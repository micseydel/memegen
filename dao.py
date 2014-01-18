from bson.objectid import ObjectId

ID = "_id"
FILENAME = "filename"
IMAGE = "image"
MEME_TEXT = "meme_text"


def get_images(db):
    "returns a list of image records"
    return db.images.find()


def get_image_filename(db, _id):
    "returns precisely one string as filename, or None if _id not found"
    result = db.images.find({ID: ObjectId(_id)})
    return result[0][FILENAME] if result else None


def get_memes(db):
    "get ALL THE MEMES"
    return db.memes.find()


def create_meme(db, image_id, meme_text):
    "returns meme id of the meme created in the database"
    return db.memes.insert({IMAGE: image_id, MEME_TEXT: meme_text})
