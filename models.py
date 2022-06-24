"""Models for Blogly."""
from unicodedata import name
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
        return f"id: {self.id}, title: {self.title}, content: {self.content}, created: {self.created_at} user_id: {self.user_id} writer: {self.writer} tags: {self.tags}"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'SET NULL'))
    writer = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')

class Tag(db.Model):
    __tablename__ = 'tag'

    def __repr__(self):
        return f'id: {self.id} name: {self.name} posts: {self.posts}'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False)

class Post_Tag(db.Model):
    __tablename__ = 'post_tag'

    def __repr__(self):
        return f'post_id: {self.post_id} tag_id: {self.tag_id}'

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('post.id', ondelete='CASCADE'), 
                        primary_key = True
                        )
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tag.id', ondelete='CASCADE'),
                        primary_key = True)
    




