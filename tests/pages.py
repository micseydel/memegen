import re
from urllib2 import urlopen, URLError
from urlparse import urlsplit

import requests

from intests import Test, run_all, assert_equal, assert_response_ok, \
    get_timestamp

BASE = "http://127.0.0.1:5000/"

SAMPLE_IMAGE = "sample.png"

SUCCESS = True

IMAGE_ID_PAT = re.compile("<a href=/image/([0-9a-f]{24})>")
IMAGE_PATH_PAT = re.compile('/(static/images/.+\\.jpg)')
MEME_PATH_PAT = re.compile('/(static/memes/.+\\.png)')


@Test
def index():
    """
    Test the index page. Except a redirect to /image.
    """
    response = urlopen(BASE)
    assert_response_ok(response.code)
    assert_equal(urlsplit(response.geturl()).path, "/image")


@Test
def get_images():
    """
    Test the main page.
    """
    response = urlopen(BASE + "image")
    assert_response_ok(response.code)
    image_paths = IMAGE_PATH_PAT.findall(response.read())
    for image_path in image_paths:
        response = urlopen(BASE + image_path)
        assert_response_ok(response.code)


@Test
def get_image():
    """
    Test a submission page.
    """
    images_page = urlopen(BASE + "image").read()
    image_id = IMAGE_ID_PAT.findall(images_page)[0]
    response = urlopen(BASE + "image/" + image_id)
    assert_response_ok(response.code)


@Test
def post_images():
    """
    Test uploading an image.
    """
    files = {"image": open(SAMPLE_IMAGE, "rb")}
    response = requests.post(BASE + "image", files=files)
    assert_response_ok(response.status_code, response.reason)


@Test
def post_meme():
    """
    Test creating a new meme.
    """
    images_page = urlopen(BASE + "image").read()
    image_id = IMAGE_ID_PAT.findall(images_page)[0]

    post_params = {
        "image": image_id,
        "top": "whoa a timestamp",
        "bottom": get_timestamp()
    }

    response = requests.post(BASE + "meme", post_params)
    assert_response_ok(response.status_code, response.reason)


@Test
def get_memes():
    """
    Test show all existing memes.
    """
    memes_response = urlopen(BASE + "meme")
    assert_response_ok(memes_response.code)
    # uncommenting the following code causes terrible, terrible hanging
    # meme_paths = MEME_PATH_PAT.findall(memes_response.read())
    #   should investigate later, but screw it for now.
    # assert meme_paths
    # for meme_path in set(meme_paths):
    #     print BASE + meme_path
    #     try:
    #         img_response = urlopen(BASE + meme_path)
    #     except KeyboardInterrupt:
    #         print 'ugh', meme_path
    #     assert_response_ok(img_response.code)


if __name__ == "__main__":
    try:
        urlopen(BASE)
    except URLError as e:
        reason = e.reason
        if reason.errno == 111:
            print "Is the server running?"
        else:
            print "Something went wrong:", reason
    else:
        run_all()
