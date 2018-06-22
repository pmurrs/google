# [START app]
import logging
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, render_template, jsonify
from base64 import b64decode
import requests
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
from google.cloud import storage


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = ['jpg','jpeg','png']

#app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['APPLICATION_ROOT'] = dirname(APP_ROOT)
UPLOAD_FOLDER = APP_ROOT
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/old',methods = ['POST', 'GET'])
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
    if len(lst) > 1:
        lst[1] = lst[1].replace(',','')
        t2 = open("Output3.txt", "w")
        text_file = open("Output4.txt", "w")
        text_file.write(lst[1].replace("'","").strip())
        t2.write(str(request.form))
        text_file.close()
        t2.close()
    else:
        print(str(request.form))

    with open('imageToSave.jpg', 'wb') as fh:
        # Get only revelant data, deleting "data:image/png;base64,"
        if len(lst) > 1:
            data = lst[1].replace("'","")
            fh.write(data.decode('base64'))

    response = jsonify({'status': 'success'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

@app.route('/image/<img>')
def _image(img):

    client = storage.Client()
    bucket = client.get_bucket('canadiantired')
    blob = bucket.blob(img)
    blob.upload_from_filename(img)
   
    # with open(image_filename, 'rb') as image_file:
    #         content_json_obj = {
    #             'content': base64.b64encode(image_file.read()).decode('UTF-8')
    #        }

    return 'Uploaded'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect("/image/" + filename, code=302)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
