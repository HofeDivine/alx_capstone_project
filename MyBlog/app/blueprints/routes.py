# from flask_login import LoginManager,login_user
# from flask import request, render_template, redirect, url_for, flash
# # from MyBlog.app import forms
# # from MyBlog.app.forms import LoginForm
#from app import app, db
# from app.models import User
# from flask_bcrypt import Bcrypt
# from app import login_manager

#bcrypt = Bcrypt(app)
from flask import Blueprint, current_app, request, render_template, redirect, url_for, flash
from  app.extensions import db, bcrypt, login_manager
from app.models import User,CreateBlog
from flask_login import login_required,current_user,logout_user
from app.decorators import custom_login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os


from flask_login import login_user
bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Check if username already exists
        # user = User.query.filter_by(username=username).first()
        # # email = User.query.filter_by(email=email).first()
        # if user :
        #     flash('Username already exists. Please choose a different one.')
        #     return redirect(url_for('register'))
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists. Please choose a different one.')
            else:
                flash('Email address is already in use. Please choose a different one.')
            return redirect(url_for('routes.register'))
        
        # If username does not exist, proceed to create new user
        # hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, email=email, password=hashed_password) 
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('routes.home'))
    
    # If method is GET, or if there's an error, show the registration form
    return render_template('register.html')

@bp.route('/login' , methods=['GET','POST'])
def userlogin():
   if request.method == 'POST':
       username = request.form['username']
       email = request.form['email']
       password = request.form['password']
       
       existing_user_query = User.query.filter((User.username == username) | (User.email == email)).first()

       if existing_user_query:
            existing_user = existing_user_query  # Retrieve the user object from the query result
            if bcrypt.check_password_hash(existing_user.password, password):
                login_user(existing_user)
                return redirect(url_for('routes.home'))
            else:
        # Password is incorrect
                return redirect(url_for('routes.userlogin'))
       else:   
    # User does not exist
             return render_template('login.html')
       
   return render_template('login.html')
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.userlogin'))
@bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(current_user.id)
    blog_posts = CreateBlog.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=user, blog_posts=blog_posts)
@bp.route('/create_post', methods=['GET', 'POST'])
@custom_login_required
def createPost():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')
        # Extract user ID from the current user's session
        author_id = current_user.id
        date_posted = datetime.utcnow()
        
                # Create new blog post with the correct author ID
        new_post = CreateBlog(title=title, content=content, user_id=author_id, date_posted=date_posted)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('routes.home'))  # Redirect to home page after successful post creation
        # If picture filename is empty or not present in request.files
        

    else:
        # Render the form template for creating a blog post
        return render_template('blogpost.html')
    
# The view routes
@bp.route('/allBlogs')
def displalAllBlogs():
    blogs = CreateBlog.query.order_by(CreateBlog.date_posted.desc()).all()
    return render_template('displayblogs.html',blogs= blogs)
@bp.route('/blog/<int:user_id>')
def View(user_id):
    #user = User.query.get_or_404(id)
    blog = CreateBlog.query.filter_by(user_id=user_id).all()
    return render_template('view.html',blogs=blog)


# @bp.route('/search')
# def search():
#     query = request.args.get('query')
#     # Perform the search query using the query string
#     # You can search the blog posts based on keywords or categories
#     results = CreateBlog.query.filter(CreateBlog.title.ilike(f'%{query}%')).all()
#     # Or: results = CreateBlog.query.filter(CreateBlog.category.ilike(f'%{query}%')).all()
#     # Render a template to display the search results
#     return render_template('searchResults.html', results=results, query=query)

