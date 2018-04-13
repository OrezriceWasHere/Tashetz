import requests
import ImageHandler

def parseTashets(image_locaion):


    url = 'https://content-vision.googleapis.com/v1/images:annotate?key=AIzaSyA---60QEj1665wtX-iEJ0YSeDZR4dRvmw&alt=json'

    base64_encodedImage = ImageHandler.handleImage(image_locaion)

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