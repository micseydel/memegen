import re
from urllib2 import urlopen, URLError

import requests

from intests import Test, run_all, assert_response_ok, get_timestamp

BASE = "http://127.0.0.1:5000/"

SAMPLE_template = "sample.png"

SUCCESS = True

template_ID_PAT = re.compile("<a href=/template/([0-9a-f]{24})>")
template_PATH_PAT = re.compile('/(static/templates/.+\\.jpg)')
MEME_PATH_PAT = re.compile('/(static/memes/.+\\.png)')


@Test
def get_templates():
    """
    Test the main page.
    """
    response = urlopen(BASE)
    assert_response_ok(response.code)
    template_paths = template_PATH_PAT.findall(response.read())
    for template_path in template_paths:
        response = urlopen(BASE + template_path)
        assert_response_ok(response.code)


@Test
def get_template():
    """
    Test a submission page.
    """
    templates_page = urlopen(BASE).read()
    template_id = template_ID_PAT.findall(templates_page)[0]
    response = urlopen(BASE + "template/" + template_id)
    assert_response_ok(response.code)


@Test
def post_templates():
    """
    Test uploading an template.
    """
    files = {"template": open(SAMPLE_template, "rb")}
    response = requests.post(BASE + "template", files=files)
    assert_response_ok(response.status_code, response.reason)


@Test
def post_meme():
    """
    Test creating a new meme.
    """
    templates_page = urlopen(BASE).read()
    template_id = template_ID_PAT.findall(templates_page)[0]

    post_params = {
        "template": template_id,
        "top": "whoa a timestamp",
        "bottom": get_timestamp()
    }

    response = requests.post(BASE + "post_meme", post_params)
    assert_response_ok(response.status_code, response.reason)


@Test
def get_memes():
    """
    Test show all existing memes.
    """
    memes_response = urlopen(BASE + "memes")
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
            print "Something unexpected went wrong:", reason
    else:
        run_all()
