# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
# from wtforms.validators import DataRequired,Email

# class LoginForm(FlaskForm):
#     username = StringField('Username',validators=[DataRequired()])
#     email = StringField('Email',validators=[DataRequired(),Email()])
#     password= PasswordField('Password',validators=[DataRequired()])
#     submit =SubmitField('Login')
from app.models import CreateBlog  # Import your model

# Query to retrieve all blog posts
blogs = CreateBlog.query.all()

# Loop through each blog post and print its id and title
for blog in blogs:
    print(f"Blog ID: {blog.id}, Title: {blog.title}")
