
from __future__ import division

import base64
import io
import cStringIO

from PIL import Image

IMAGE_WIDTH = 4032
IMAGE_HEIGHT = 3024

IMAGE_RATIO = IMAGE_WIDTH / IMAGE_HEIGHT

IMAGE_NEW_HEGIHT = 1000
IMAGE_NEW_WIDTH = int(IMAGE_NEW_HEGIHT * IMAGE_RATIO)

def handleImage(imageDir):


    image = Image.open(imageDir)

    resizeImage(image)



    return encodeImage(image)


def resizeImage(image):

    print "resizing image..."
    image = image.resize((IMAGE_NEW_WIDTH, IMAGE_NEW_HEGIHT), Image.ANTIALIAS)
    print "done."
    pass


def encodeImage(image):

    buffer = cStringIO.StringIO()
    image.save(buffer, format="JPEG")

    print "encoding base 64..."

    coded = base64.b64encode(buffer.getvalue())

    print "done."

    return coded
