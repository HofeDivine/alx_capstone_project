from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blog_posts = db.relationship('CreateBlog', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class CreateBlog(db.Model):
    __tablename__ = 'CreateBlog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    picture_path = db.Column(db.String(255))  # Field to store the file path
    category = db.Column(db.String(50))
    def __repr__(self):
        return f"BlogPost('{self.title}', '{self.date_posted}')"
class CreateComments(db.Model):
    __tablename__ = 'CreateComments'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable = False)
    
