#!/usr/bin/env python

import os, sys, json
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, Response
from werkzeug import secure_filename
from ocr_funcs import scan_letter_from_api

# Initialisation de Flask et de l'API
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'bmp'])
dn = os.path.dirname(os.path.realpath(__file__))

# Fonction qui verifie si l'extension du fichier est autorisee
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# http://localhost:5000/
@app.route('/')
def index():
    return "OCR API - bartho_c, crouze_t, mombul_s, wirstz_j\n"

# http://localhost:5000/ocr/api/v1.0/scan_letter
@app.route('/ocr/api/v1.0/scan_letter', methods=['POST'])
def scan_letter():
    fileimg = request.files['img'] # On recupere le fichier 
    token = "ocrepitech" # et le token
    authtoken = "ocrepitech"
    
    if fileimg and allowed_file(fileimg.filename) and token == authtoken: # Si le fichier est autorise...
        filename = secure_filename(fileimg.filename)
        fileimg.save(dn + '/' + app.config['UPLOAD_FOLDER'] + filename) # on save le fichier
        json_res = scan_letter_from_api(dn + '/' + app.config['UPLOAD_FOLDER'] + filename) # on envoie le fichier a l'OCR
        json_res = jsonify(json_res)
        data = json_res.data
        
        os.remove(dn + '/' + app.config['UPLOAD_FOLDER'] + filename)
        resp = Response(data, status=201, mimetype="application/json")
    else:
        data = {'result': '', 'error': 'Bad request'}
        resp = Response(data, status=400, mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
