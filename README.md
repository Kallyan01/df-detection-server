# Documentation
Start the venv by this command
```python
python3 -m venv env
source ./env/bin/activate
```
Install deps
```python
pip install -r requirements.txt
```

## ENV setup deps
add ```.env.dev``` & ```.env.prod``` to directory

```python
export FLASK_ENV=dev #for development server 
#or
export FLASK_ENV=prod #for production server
```

## Run locally

```shell
celery -A celery_worker worker --loglevel=INFO
python3 run.py
```


## Build Docker Image 
```shell
sudo docker build -t build-server . 
```

## Run Docker image

```shell
sudo docker run --gpus all df-server
```

