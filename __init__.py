from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = 'jshf763fbdhcp9NJKDEGERGVFD'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/phongmach?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

login = LoginManager(app=app)

db = SQLAlchemy(app=app)

babel = Babel(app=app)


@babel.localeselector
def get_locate():
    return 'vi'