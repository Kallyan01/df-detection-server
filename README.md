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
## Build Docker Image 
```shell
sudo docker build -t build-server . 
```
```
## Run Docker image 
```shell
sudo docker run --gpus all df-server```

