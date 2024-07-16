This document records all the codes and information of this project while using the cloud service

// Things to install in EC2 ubuntu


sudo apt-get update
sudo apt install -y python3-pip nginx
pip install --upgrade pip setuptools wheel
sudo vim /etc/nginx/sites-enabled/fastapi_nginx

server {
        listen 80;
        server_name 57.180.8.175;

        location / {
                proxy_pass http://127.0.0.1:8000;
        }

        location /backup/ {
                root /var/www/html;
                index new_web.html;
        }

}

sudo service nginx restart

git clone https://github.com/garfieldtong/Event_tool.git

*need to move the new_web.html to /var/www/html/backup/ in advance

sudo apt install python3.10-venv     // need to use venv, or else it can't find fastapi package
python3 -m venv "CMP"
cd CMP
source bin/activate
cd ~/Event_tool/everything_bug/code
pip3 install -r requirements.txt
screen fastapi run app/updated.py --host 127.0.0.1 --port 8000


//About screen session

screen -ls   // list all screen sessions
screen -XS <session-id> quit     // kill selected screen session
screen -r <session-id>     // reattach to screen session

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





