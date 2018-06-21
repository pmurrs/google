# [START app]
import logging
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, render_template, jsonify
from base64 import b64decode
import requests


#app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods = ['POST', 'GET'])
@cross_origin()
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/test',methods = ['POST', 'GET'])
@cross_origin()
def test():
    #print request.data
    print('aaaaaaaaaa')
    lst = str(request.form).split(',')
    lst[1] = lst[1].replace(',','')
    t2 = open("Output3.txt", "w")
    text_file = open("Output4.txt", "w")
    text_file.write(lst[1].replace("'","").strip())
    t2.write(str(request.form))
    text_file.close()
    t2.close()

    with open('imageToSave.jpg', 'wb') as fh:
        # Get only revelant data, deleting "data:image/png;base64,"
        data = lst[1].replace("'","")
        fh.write(data.decode('base64'))

    response = jsonify({'status': 'success'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

@app.route('/image')
def _image(input_file, output_file):
   
    with open(image_filename, 'rb') as image_file:
            content_json_obj = {
                'content': base64.b64encode(image_file.read()).decode('UTF-8')
            }
    return 'Hello World!'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
