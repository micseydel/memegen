import requests
from urllib2 import urlopen, URLError
from urlparse import urlsplit

from intests import Test, run_all, assert_equal, assert_response_ok, \
    assert_untested, get_timestamp

BASE = 'http://127.0.0.1:5000/'

SAMPLE_IMAGE = "sample.png"

SUCCESS = True


@Test
def index():
    '''
    Test the except page. Except a redirect to /image.
    '''
    response = urlopen(BASE)
    assert_response_ok(response.code)
    assert_equal(urlsplit(response.geturl()).path, '/image')


@Test
def get_images():
    '''
    Test the main page.
    '''
    response = urlopen(BASE + 'image')
    assert_response_ok(response.code)


@Test
def get_image():
    '''
    Test a submission page.
    '''
    response = urlopen(BASE + 'image/1')
    assert_response_ok(response.code)


@Test
def post_images():
    '''
    Test uploading an image.
    '''
    files = {'image': open(SAMPLE_IMAGE, 'rb')}
    response = requests.post(BASE + 'image', files=files)
    assert_response_ok(response.status_code, response.reason)


@Test
def get_meme():
    '''
    Test getting a saved meme. Redirects.
    '''
    response = urlopen(BASE + 'meme/1')
    assert_equal(response.geturl(), BASE + 'static/memes/1.png')
    assert_response_ok(response.code)


@Test
def get_memes():
    '''
    Test show all existing memes.
    '''
    response = urlopen(BASE + 'meme')
    assert_response_ok(response.code)


@Test
def post_meme():
    '''
    Test creating a new meme
    '''
    post_params = {
        'image': '1',
        'top': 'whoa a timestamp',
        'bottom': get_timestamp()
    }
    response = requests.post(BASE + 'meme', post_params)
    assert_response_ok(response.status_code, response.reason)


if __name__ == '__main__':
    try:
        urlopen(BASE)
    except URLError as e:
        reason = e.reason
        if reason.errno == 111:
            print 'Is the server running?'
        else:
            print 'Something went wrong:', reason
    else:
        run_all()
