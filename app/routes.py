from flask import request, jsonify
import os
import redis 
from app.functions.schema_validation import isPredictDataValid
from app.functions.helper import hash_url
from app import app ,celery
from app.functions.tasks.predict import predictvid , process_task , upload_file

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#rd = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['video'] 
        print(file)
        if not file:
         return {"error": 'File upload unsuccessful ! Try Again'}
        path_to_videos = []
        path_to_videos.append(upload_file(file))
        print(path_to_videos)
        task = predictvid.apply_async(kwargs={'path': path_to_videos})
        return jsonify({'process_id': task.id}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500
#    data = request.json
 #   if not isPredictDataValid(data):
  #      return jsonify({'error': 'Data is not valid'}) ,400
 #   if not data:
 #        return jsonify({'error': 'No JSON data received'}), 400
 #   rd_data = rd.get(hash_url(data['video_url']))

  #  if rd_data is not None:
   #     print(rd_data)
        
    #    return jsonify({"prediction":rd_data}), 200
   # else:
    #    rd.set(hash_url(data['video_url']), data['video_url'])
    #    return data,200;


@app.route('/status/<task_id>', methods=['GET'])
def get_task_result(task_id):
    try:
        result = celery.AsyncResult(task_id)
        task_status = result.status

        if task_status == 'SUCCESS':
            task_result = result.get()
            return jsonify({'status': task_status, 'result': task_result}), 200
        elif task_status == 'FAILURE':
            error_message = result.traceback
            return jsonify({'status': task_status, 'error': error_message}), 500
        else:
            return jsonify({'status': task_status}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500
     


@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

@app.route('/ping', methods=['GET'])
def ping():
   # rd.set('ping', 'pong')
    return jsonify({'message': 'pong'})



@app.route('/hit', methods=['GET'])
def demo_endpoint():
    try:
        task = process_task.delay()
        return jsonify({'task_id': task.id}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

