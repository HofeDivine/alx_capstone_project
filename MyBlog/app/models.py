"""This is for defining our user models
User class defines what goes into our user table 
"""
from sqlalchemy import Nullable
from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blog_posts = db.relationship('CreateBlog', backref='author', lazy=True,cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class CreateBlog(db.Model):
    __tablename__ = 'CreateBlog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    picture = db.Column(db.LargeBinary)  
    category = db.Column(db.String(50))
    def __repr__(self):
        return f"BlogPost('{self.title}', '{self.date_posted}')"
class CreateComments(db.Model):
    __tablename__ = 'CreateComments'
    content = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text, nullable=False)
    
    # Foreign key to link comments to the corresponding blog post
    post_id = db.Column(db.Integer, db.ForeignKey('CreateBlog.id'), nullable=False)
    
    # Relationship attribute to access the associated blog post
    post = db.relationship('CreateBlog', backref=db.backref('comments', lazy=True,cascade="all, delete"))

    def __repr__(self):
        return f"Comment('{self.content}')"

    

class BlogVideo(db.Model):
    __tablename__ = 'BlogVideo'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('CreateBlog.id'), nullable=False)
    blog = db.relationship('CreateBlog', backref=db.backref('videos', lazy=True))

class BlogLink(db.Model):
    __tablename__ = 'BlogLink'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('CreateBlog.id'), nullable=False)
    blog = db.relationship('CreateBlog', backref=db.backref('links', lazy=True))
class BlogImage(db.Model):
    __tablename__ = 'BlogImage'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('CreateBlog.id'), nullable=False)
    blog = db.relationship('CreateBlog', backref=db.backref('images', lazy=True))
