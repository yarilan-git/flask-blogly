"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'

    def __repr__(self):
        return f"id: {self.id}, f_name: {self.first_name}, l_name: {self.last_name}, url: {self.image_url}"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(30),
                           nullable = False)
    last_name = db.Column(db.String(30),
                          nullable = False)
    image_url = db.Column(db.String(100))

class Post(db.Model):
    __tablename__ = 'post'

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}, content: {self.content}, created: {self.created_at} user_id: {self.user_id} writer: {self.writer}"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship('User', backref='posts')

