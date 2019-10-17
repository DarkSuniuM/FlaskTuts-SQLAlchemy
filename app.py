from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_tuts:123456@localhost/flask_tuts_11'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    


@app.route('/')
def index():
    action = request.args.get('action')
    username = request.args.get('username')
    password = request.args.get('password')
    if action and username and password:
        if action.lower() == 'register':
            new_user = User()
            new_user.username = username
            new_user.password = password
            try:
                db.session.add(new_user)
                db.session.commit()
                return "User added."
            except IntegrityError:
                db.session.rollback()
                return "User duplicated."
        if action.lower() == 'login':
            user = User.query.filter(User.username == username, User.password == password).first()
            print(user.id)
            print(user.username)
            print(user.password)
            if not user:
                return "Invalid Credentions"
            return f"Welcome dear {user.username}"
    return "Hello World!"


# ORM => Object Relational Mapper
# SQLAlchemy
