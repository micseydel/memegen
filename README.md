memegen
=======

In House Meme Generator

This was designed to be drop and use as much as possible, but my changes aren't keeping with that. I may move back in that direction later, but for now it's aimed toward being office-specific.

To Run:
```bash
python injokes.py
```

Features
========
* New Image Template Upload
* Creates static links for all memes generated

Planned Features
================
* Users, tagging of users, up votes of popular memes, etc.

How It Works
============

Memegen stores all images on the local file system in the static/images and static/memes folders.  A mongodb is used to keep track of everything.

Memegen uses PIL (Python Image Library) to write text on images.

http://flask.pocoo.org/docs/deploying/

Dependencies
============
All the dependencies can be installed via pip

```bash
sudo apt-get install python-pip python-dev build-essential libjpeg8-dev
sudo pip install pillow
sudo pip install flask
sudo pip install Flask-PyMongo
```

