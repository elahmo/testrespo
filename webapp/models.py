from webapp import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName: {self.username}"

class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    tip = db.Column(db.String)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, tip, text, user_id):
        self.title = title
        self.tp = tip
        self.text = text
        self.user_id = user_id

    def __repr__(self):

        return f"post id: {self.id}"

class Leader(db.Model):
    __tablename__ = 'leaders'

    field1 = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Team = db.Column(db.Text)
    Gamesplayed = db.Column(db.Integer)
    AverageMin = db.Column(db.Float)
    FGM = db.Column(db.Float)
    FGA = db.Column(db.Float)
    FG_ = db.Column('FG%', db.Float)
    _3PM = db.Column('3PM', db.Float)
    _3ATT = db.Column('3ATT', db.Float)
    _3PT_ = db.Column('3PT%', db.Float)
    FTM =  db.Column(db.Float)
    FTA = db.Column(db.Float)
    FT_ = db.Column('FT%',db. Float)
    OREB = db.Column(db.Float)
    DREB = db.Column(db.Float)
    REB = db.Column(db.Float)
    AST = db.Column(db.Float)
    STL = db.Column(db.Float)
    BLK = db.Column(db.Float)
    TOV = db.Column(db.Float)
    PPG = db.Column(db.Float)

class Daily(db.Model):

    __tablename__ = 'daily'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class News(db.Model):

    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    heading = db.Column(db.String)
    article = db.Column(db.String)
    pic = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
