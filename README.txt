# Instructions
This document records all the codes and information of this project through **setting up a local server**

git clone https://github.com/garfieldtong/Event_tool.git

## Using venv as virtual environment
```
sudo apt install python3.10-venv
python3 -m venv "CMP"
cd CMP
source bin/activate
cd ~/Event_tool/everything_bug/code
pip3 install -r requirements.txt
```

## Activate server
```
fastapi run app/updated.py --host 127.0.0.1 --port 8000
```

// Test for docker

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





