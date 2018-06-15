import ParseImage
import flask
import OCRhandler
import json

app = flask.Flask(__name__)

@app.route('/getTashetzParseImage', methods=['POST'])
def getParseImageTashetz():

    google_analsis_data = flask.request.values.get('google_analysis')
    image_data = flask.request.values.get('base_64_image')

    if google_analsis_data is None and image_data is None:

        return json.dumps({ "error": "no data provided. please provide data on either" +
                                     " 'google_analysis' or 'base_64_image' parameters" }), 400

    if image_data is not None:
        google_analsis_data = OCRhandler.parseTashets(image_bytes=image_data)

    return json.dumps({"result" : ParseImage.parseGoogleText(google_analsis_data)}), 200

app.run(port=80, debug=True)
