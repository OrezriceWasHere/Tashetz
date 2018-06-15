import requests
import ImageHandler


def parseTashets(image_bytes=None, image_locaion=None):

    if image_bytes is None and image_locaion is None:
        raise ValueError("Need to have at least one parameter")


    url = 'https://content-vision.googleapis.com/v1/images:annotate?key=AIzaSyA---60QEj1665wtX-iEJ0YSeDZR4dRvmw&alt=json'

    base64_encodedImage = ImageHandler.handleImage(image_locaion) if image_bytes is None else image_bytes

    parameters =  {
        "requests": [
            {

                "image": {
                    "content" : base64_encodedImage
                },

                "features": [
                    {
                      "maxResults": 1,
                      "type": "TEXT_DETECTION"
                    }
                ],

                "imageContext": {
                    "languageHints": ["he"]
                }
            }
        ]
    }


    print "sending image to google..."


    response =  requests.post(url, json=parameters).text

    print "done."

    return response