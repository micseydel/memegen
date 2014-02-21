from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)

FONT_PATH = "static/fonts/Impact.ttf"


def gen_meme(image_name, top, bottom, meme_id):
    top = top.upper()
    bottom = bottom.upper()
    image_path = os.path.join('static/templates', image_name)

    img = Image.open(image_path)
    imageSize = img.size

    # find biggest font size that works
    fontSize = imageSize[1] / 5
    font = ImageFont.truetype(FONT_PATH, fontSize)
    topTextSize = font.getsize(top)
    bottomTextSize = font.getsize(bottom)
    while topTextSize[0] > imageSize[0] - 20 or \
            bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(FONT_PATH, fontSize)
        topTextSize = font.getsize(top)
        bottomTextSize = font.getsize(bottom)

    # find top centered position for top text
    topTextPosition = (imageSize[0] / 2 - topTextSize[0] / 2, 0)

    # find bottom centered position for bottom text
    bottomTextPositionX = imageSize[0] / 2 - bottomTextSize[0] / 2
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    draw = ImageDraw.Draw(img)

    # draw outlines
    # there may be a better way
    outlineRange = fontSize / 15
    for x in xrange(-outlineRange, outlineRange + 1):
        for y in xrange(-outlineRange, outlineRange + 1):
            draw.text((topTextPosition[0] + x, topTextPosition[1] + y),
                      top, WHITE, font=font)
            draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y),
                      bottom, WHITE, font=font)

    draw.text(topTextPosition, top, BLACK, font=font)
    draw.text(bottomTextPosition, bottom, BLACK, font=font)

    img.save("static/memes/%s.png" % meme_id)
