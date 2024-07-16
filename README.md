# Instructions
This document records all the codes and information of this project through **setting up a local server**

## 1. Clone repo
```
git clone -b local https://github.com/garfieldtong/Event_tool.git
```

## 2. Set up virtual environment

Set up either using venv or conda

**venv:**
```
sudo apt install python3.10-venv
python3 -m venv "CMP"
cd CMP
source bin/activate
cd Event_tool/code
pip3 install -r requirements.txt
```

**conda:**
```
conda create -n CMP python=3.10
conda activate CMP
cd Event_tool/code
pip install -r requirements.txt
```

## 3. Activate server
```
fastapi run app/updated.py --host 127.0.0.1 --port 8000
```

## 4. Open the web in Event_tool/phone/new_web.html
As this tool was devloped as a mobile application, use the developer tool in your browser and choose "Toggle device toolbar" (or just press Ctrl+Shift+M) to view as a device.

## Using Docker for setup (optional)
```
docker build -t proj_test .
docker run -d --name proj_test -p 8000:8000 proj_test

docker ps -a

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

docker build -t proj_test .
docker run -d --name proj_test -p 8000:8000 proj_test

docker build -t proj_test:1.0.0 .
docker run -p 8000:8000 proj_test:1.0.0

docker image tag proj_test:1.0.0 c8n.io/garfieldcm385/proj_test

docker push c8n.io/garfieldcm385/proj_test
```




