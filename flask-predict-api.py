#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:06:35 2018

@author: vivekkalyanarangan
"""

import pickle
from flask import Flask, request
# from flasgger import Swagger
import numpy as np
import pandas as pd
import json

with open('nba_metamediamodels/models/rf.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)
# swagger = Swagger(app)

@app.route('/predict',methods=["GET"])
def predict_iris():
    """Example endpoint returning a prediction of iris
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
    """
    s_length = request.args.get("s_length")
    s_width = request.args.get("s_width")
    p_length = request.args.get("p_length")
    p_width = request.args.get("p_width")
    
    prediction = model.predict(np.array([[float(s_length), float(s_width), float(p_length), float(p_width)]]))
    proba = np.amax(model.predict_proba(np.array([[float(s_length), float(s_width), float(p_length), float(p_width)]])))
    pred_string = 'We Predict category {}, with a probability of {}%.'.format(prediction[0],str(100*round(proba,3)))
    pred_dict = {
                    "VALUE":int(prediction[0]),
                    "PROBABILITY":float(proba)
                }
    pred_json = json.dumps(pred_dict)

    return pred_json

@app.route('/predict_file', methods=["POST"])
def predict_iris_file():
    """Example file endpoint returning a prediction of iris
    ---
    parameters:
      - name: input_file
        in: formData
        type: file
        required: true
    """
    file = pd.read_json(request.files.get("input_file"))
    return str(file)
    # input_dict = dict(json.loads(file))
    # input_df = pd.DataFrame.from_records(input_dict)
    # prediction = model.predict(input_data)
    # proba = np.amax(model.predict_proba(input_data))
    # pred_string = 'We Predict category {}, with a probability of {}%.'.format(prediction[0],str(100*round(proba,3)))
    # pred_dict = {
    #                 "VALUE":int(prediction[0]),
    #                 "PROBABILITY":float(proba)
    #             }
    # pred_json = json.dumps(pred_dict)

    # return pred_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    