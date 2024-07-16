# インストール
## 1. リポジトリをクローンする
```
git clone -b local https://github.com/garfieldtong/Event_tool.git
```

## 2. Pythonの仮想環境作成

venv または conda　のいずれかを使用します。

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

## 3. サーバー構築
```
fastapi run app/updated.py --host 127.0.0.1 --port 8000
```

## 4. Event_tool/phone/new_web.htmlでサイトを起動
このツールはモバイル端末向けに最適化されています。パソコンでご利用の場合は、ブラウザの開発者ツールを使って携帯表示モードに切り替えることをおすすめします。<br>
切り替え方法は以下の通りです：<br>
1.ブラウザの開発者ツールを開く（F12キーを押す）<br>
2.'Toggle device toolbar'を選択する（または Ctrl+Shift+M を押す）


