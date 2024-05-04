from flask import request, jsonify
import os
import redis 
from app.functions.schema_validation import isPredictDataValid
from app.functions.helper import hash_url
from app import app
from app.functions.tasks.predict import predictvid

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
rd = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/predict', methods=['POST'])
def predict():
    return predictvid()
    data = request.json
    if not isPredictDataValid(data):
        return jsonify({'error': 'Data is not valid'}) ,400
    if not data:
         return jsonify({'error': 'No JSON data received'}), 400
    rd_data = rd.get(hash_url(data['video_url']))

    if rd_data is not None:
        print(rd_data)
        
        return jsonify({"prediction":rd_data}), 200
    else:
        rd.set(hash_url(data['video_url']), data['video_url'])
        return data,200;


  
     


@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

@app.route('/ping', methods=['GET'])
def ping():
    rd.set('ping', 'pong')
    return jsonify({'message': 'pong'})

