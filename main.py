import os
import sys
import re
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

#set the path that the upload file will store
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    os.system('python cassandra.py')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            global filename, output
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           
            recognized = os.popen('python recognize.py '+app.config['UPLOAD_FOLDER']+filename) # return file
            output = recognized.read()
            recognized.close()
            predict=re.findall(r"\d+\.?\d*",output)
            os.system('python cassandra-connect.py '+filename+' '+predict[0])
            return output
        return '<p> You uploaded an impermissible file type </p>' #redirect to preview page
    return '''
    <!doctype html>
    <title>MNIST-recognize</title>
    <h1>MNIST-recognize</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

#view the file user uploaded
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#record data and store into the keyspace of cassandra upload_time, image_name, recognize_number
@app.route('/record')
def data_record():
    predict=re.findall(r"\d+\.?\d*",output)
    os.system('python cassandra-connect.py '+filename+' '+predict[0])
    return "data stored"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
    #app.run()
