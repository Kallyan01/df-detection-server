import json
from flask import request, jsonify
import os
from app.functions.schema_validation import isPredictDataValid
from app.functions.helper import hash_url
from app import app ,celery ,redis_result_cache_db ,redis_uuid_map_db
from app.functions.tasks.predict import predictvid , process_task , upload_file
import uuid
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#rd = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'video' not in request.files :
            return jsonify({'error': 'Video file not provided'}), 400
        if 'url' not in request.form :
            return jsonify({'error': 'JSON data not provided'}), 400
        file = request.files['video']
        url = request.form['url']
        print("uo")
        hashed_url = str(hash_url(url))
        print(hashed_url)
        result_exist = redis_result_cache_db.get(hashed_url)
        print(result_exist)
        if result_exist:
            process_id = str(uuid.uuid1())
            redis_uuid_map_db.set(process_id, hashed_url)
            return jsonify({'process_id': process_id, 'message': 'result exist'}), 200
        else:
            if not file:
                return jsonify({'error': 'File upload unsuccessful! Try Again'}), 400
            
            path_to_videos = [upload_file(file)]
            task = predictvid.apply_async(kwargs={'path': path_to_videos})
            redis_uuid_map_db.set(task.id,hashed_url)
            return jsonify({'process_id': task.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
#    
 #   
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
        # Retrieve URL hash from Redis
        url_hash_bytes = redis_uuid_map_db.get(task_id)
        print(url_hash_bytes)
        # Check if the URL hash exists and decode it
        if url_hash_bytes:
            url_hash = url_hash_bytes.decode('utf-8') # type: ignore
            print(url_hash)
            # Retrieve the result from the cache using the URL hash
            result_exist_bytes = redis_result_cache_db.get(url_hash)
            print(result_exist_bytes)
            if result_exist_bytes:
                result = json.loads(result_exist_bytes.decode('utf-8')) # type: ignore
                print(result)
                return jsonify({'result': result, 'status': 'CACHED'}), 200

            # If the result is not in the cache, check Celery task status
            result = celery.AsyncResult(task_id, app=celery)
            task_status = result.status
            print(task_status)
            if task_status == 'SUCCESS':
                task_result = result.result
                redis_result_cache_db.set(url_hash,json.dumps(task_result))
                return jsonify({'status': task_status, 'result': task_result}), 200
            elif task_status == 'FAILURE':
                error_message = result.traceback
                redis_uuid_map_db.delete(task_id)
                return jsonify({'status': task_status, 'error': error_message}), 500
            else:
                return jsonify({'status': task_status}), 202

        # If the URL hash does not exist
        return jsonify({'status': "Invalid Process Id"}), 404
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

