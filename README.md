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
export FLASK_ENV=prod #for production server
```

## Build Docker Image 
```shell
sudo docker build -t build-server . 
```
## Run Docker image

```shell
docker run --gpus all -p 5000:5000 -d df-server \n
docker ps
```

