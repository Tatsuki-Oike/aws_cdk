from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json

import config

# 接続情報
USER = config.USER
PASSWORD = config.PASSWORD
HOST = config.HOST
DATABASE = config.DATABASE

# DB, API準備
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
db.init_app(app)
api = Api(app)

# テーブル作成
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)

# サンプルデータ作成関数
def make_data():
    db.session.query(User).delete()
    db.session.commit()
    users_list = [
        (0, "Ichiro"),
        (2, "Jiro"),
        (3, "Saburo")
    ]
    User_list = [
        User(id=id, username=name) for id, name in users_list
    ]
    db.session.bulk_save_objects(User_list)
    db.session.commit()

# API作成
class HelloWorld(Resource):
    def get(self):
        try:
            users = db.session.query(User).all()
            users_list = []
            for user in users:
                users_list.append(
                    {
                        "id": str(user.id),
                        "username": str(user.username)
                    }
                )
            response = {"Users": users_list}
        except Exception as e:
            response = {"error": str(e)}
        return json.dumps(response)

api.add_resource(HelloWorld, '/')

# サーバーの起動
if __name__ == '__main__':

    # テーブル作成, サンプルデータ作成
    with app.app_context():
        db.create_all()
        make_data()

    # サーバーの起動
    app.run(debug=True, host="0.0.0.0", port=80)