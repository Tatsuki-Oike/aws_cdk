## Pythonの仮想環境構築

```sh
cd ./aws_cdk/03_rds/flask
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

## Flask appの実行

```sh
sudo -E venv/bin/python app.py
```
