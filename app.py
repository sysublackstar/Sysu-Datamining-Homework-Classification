from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  #Use CPU for prediction if your GPU doesn't work caused by a cudnn error

app = Flask(__name__)
graph = tf.get_default_graph()
model = load_model('models/cnn.h5')

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    global graph
    with graph.as_default():
        preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = model_predict(file_path, model)
        
        if preds[0][0] < 0.5:
            result = '可回收垃圾'
        elif preds[0][0] >= 0.5:
            result = '不可回收垃圾'
        return str(result)
    return None


if __name__ == '__main__':
    # Serve the app with gevent
    http_server = WSGIServer(('127.0.0.1', 5000), app )
    http_server.serve_forever()
