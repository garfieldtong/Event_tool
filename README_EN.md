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
As this tool was devloped as a mobile application, use the developer tool in your browser and choose "Toggle device toolbar" (or press F12, then Ctrl+Shift+M) to view as a device.



