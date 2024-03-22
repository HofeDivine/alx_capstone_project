
from flask import Blueprint, current_app, request, render_template, redirect, url_for, flash,get_flashed_messages
from  app.extensions import db, bcrypt, login_manager
from app.models import CreateComments, User,CreateBlog
from flask_login import login_required,current_user,logout_user
from app.decorators import custom_login_required,strip_html_tags
from datetime import datetime




from flask_login import login_user
bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@bp.route('/')
def home():
    # flash('Welcome to EDUFUN! Where education meets fun','success')
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists. Please choose a different one.','failure')
            else:
                flash('Email address is already in use. Please choose a different one.','failure')
            return redirect(url_for('routes.register'))
       
        else:
            new_user = User(username=username, email=email, password=hashed_password) 
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. Please log in.','success')
            return redirect(url_for('routes.home'))
        
    
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
                flash("You have log in successfully","success")
                return redirect(url_for('routes.home'))
            else:
                flash('password is incorrect',"failure")
                return redirect(url_for('routes.userlogin'))
       else:   
    # User does not exist
             flash('user does not exist','failure')
             return render_template('login.html')
       
   return render_template('login.html')
@bp.route('/logout')
def logout():
    logout_user()
    flash('You have log out! Thanks for being with us','success')
    return redirect(url_for('routes.home'))
# @bp.route('/dashboard')
# @login_required
# def dashboard():
#     user = User.query.get(current_user.id)
#     blog_posts = CreateBlog.query.filter_by(user_id=current_user.id).all()
#     return render_template('dashboard.html', user=user, blog_posts=blog_posts)
@bp.route('/create_post', methods=['GET', 'POST'])
@custom_login_required
def createPost():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form.get('content')
        
        author_id = current_user.id
        date_posted = datetime.utcnow()
        
                
        new_post = CreateBlog(title=title, content=content, user_id=author_id, date_posted=date_posted)
        db.session.add(new_post)
        db.session.commit()
        flash('You have created a blog succesfully','success')
        return redirect(url_for('routes.home'))  
        

    else:
        flash('Your post is not successful! Try again','failure')
        return render_template('blogpost.html')
    

@bp.route('/allBlogs')
def displalAllBlogs():
    blogs = CreateBlog.query.order_by(CreateBlog.date_posted.desc()).all()
    return render_template('displayblogs.html',blogs= blogs)
@bp.route('/blog/<int:id>')
def View(id):
    # post_id = CreateBlog.query.get(id)
    blog = CreateBlog.query.filter_by(id=id).all()
    comments = CreateComments.query.filter_by(id=id).all()
    return render_template('view.html',blogs=blog,comments=comments)

@bp.route('/comments/<int:id>', methods=['POST','GET'])
@custom_login_required
def comments(id):
    if request.method == 'POST':
        authorName= request.form['author']
        content = request.form['content']
        new_comment = CreateComments(author=authorName,content=content,post_id=id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Thanks for your comments!','success')
        return redirect(url_for('routes.View',id=id))
    else:
         return render_template('commentPost.html', id=id)
@bp.route('/update/<int:id>', methods=['GET','POST'])
@custom_login_required
def updatePost(id):
    # Retrieve the post from the database
    post = CreateBlog.query.get_or_404(id)
    # Check if the current user is the author of the post
    if current_user.id != post.user_id:
        # Redirect to home or show an error message
        flash('You are not the author of this post','failure')
        return redirect(url_for('routes.home'))
    if request.method == 'POST':
        # Update the post with the form data
        post.title = request.form['title']
        post.content = request.form['content']
        
        # Commit the changes to the database
        db.session.commit()
        
        flash('Post updated successfully.','success')
        return redirect(url_for('routes.View',id=id))
    stripped_content = strip_html_tags(post.content)
    return render_template('updatePost.html', post=post,stripped_content=stripped_content,id=id)
@bp.route('/deletePost/<int:id>', methods=['GET'])
@custom_login_required
def deletePost(id):
    post = CreateBlog.query.get_or_404(id)

    # Ensure the current user is the author of the post
    if current_user.id != post.user_id:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('routes.home'))

    # Delete the post
    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted.', 'success')
    return redirect(url_for('routes.View',id=id))

@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        # Perform a search query based on the keyword
        # For example, you might query the database for blog posts with titles containing the keyword
        # Adjust this query based on your database schema and requirements
        blogs = CreateBlog.query.filter(CreateBlog.title.ilike(f'%{keyword}%')).all()
        return render_template('displayblogs.html', blogs=blogs, keyword=keyword)
    else:
        # If no keyword is provided, redirect to the homepage or display an error message
        flash('Please enter a keyword to search.', 'error')
        return redirect(url_for('routes.home'))



