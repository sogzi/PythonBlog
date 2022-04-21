import secrets
from PIL import Image
import os
from newblog import app, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from newblog.blogdb import Users, Posts
from newblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import update
from newblog import engine, Base, conn, session
from sqlalchemy.orm import sessionmaker




@app.route("/")
@app.route("/home")
@login_required
def home():
    s = session()
    # page = request.args.get('page', 1, type=int)
    posts = s.query(Posts, Users).join(Users).all()
    return render_template('home.html', Posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        print(email == '')
        if email == '':
            email = None



        user = Users(username=username,
                     email=email,
                     password=hash_password
                     )

        s = session()

        s.add(user)
        s.commit()

        flash('Your accont has been created! You are now able to log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    s = session()
    if form.validate_on_submit():
        user = s.query(Users).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    # return redirect(next_page) if next_page else redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    s = session()
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        s.query(Users).filter_by(username=current_user.username).update({Users.username: form.username.data,
                                                                        Users.email: form.email.data,
                                                                        Users.image_file: picture_file})
        s.commit()
        flash('Your account has been updated!', 'success')
        current_user.username = form.username.data
        current_user.email = form.email.data

    return render_template('account.html', image_file=image_file, title='Account',
                           form=form, legend='New Post')


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = current_user.id
        post = Posts(title=title, content=content, author=author)
        s = session()

        s.add(post)
        s.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('newpost.html', title='New Post', form=form)


@app.route("/post/<int:post_id>")
def postview(post_id):
    s = session()
    post = s.query(Posts).get(post_id)
    if post:
        return render_template('post.html', title=post.title, post=post)
    else:
        abort(404)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    s = session()
    post = s.query(Posts, Users).join(Users, Posts).filter(Users.id)
    # if post_id != current_user.id:
    #     abort(403)
    form = PostForm()

    if Posts.author != current_user.id:
        abort(403)
    if Posts.author != current_user.id:
        flash('Only Author can update the post', 'warning')
        return redirect(url_for('postview', post_id=post.id))
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        s.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('postview', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    s = session()
    post = s.query(Posts, Users).join(Users, Posts).filter(Users.id)
    if post_id != current_user.id:
        abort(403)
    s.delete(post)
    s.commit()
    print('shakes')
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


