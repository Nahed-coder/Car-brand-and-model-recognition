import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from resouces import tools
import cv2

import numpy as np

#tensorflow
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'nahed'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process', methods=['POST'])
def process():
    print(request.form)
    print(request.args)
    image_name = request.form.get('image_name', None)
    if image_name is not None:
        #load model
        model = load_model("./model/vgg_36.h5")

        #process image
        imgOriginal = cv2.imread(image_name)
        img = tools.process_image(imgOriginal)

        pred_data,pv = tools.predict(img=img, model=model)
        print(pred_data)
        print(pv)
        return pred_data

    return {'res': 'Error'}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print("<<<"+file.filename)
        filename = secure_filename(file.filename)
        print(filename+"====")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {'msg': 'uploaded'}


app.run(debug=True)