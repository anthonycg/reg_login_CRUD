from crypt import methods
from unittest.util import three_way_cmp
from flask_app import app
from flask_app.models import user
from flask import Flask, render_template, request, session, flash, redirect
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    #validate user's inputs
    if not user.User.validate_form(request.form):
        return redirect ('/')
    #create pw hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    #Grab data from webpage
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password']
    }
    # Save the user's inputs into the DB -- INSERT INTO
    user.User.save(data)
    #store user id into session
    session['user_id'] = user.User.save(data)
    return redirect ('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    #check if username exists in database
    data = { "email": request.form['email']}
    user_in_db = user.User.get_user_by_email(data)
    #if it doesn't, redirect to login page
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    #if username does exist, check if it matches pw hash
    #if pw doesn't match:
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    #if pw does match, redirect to dashboard -- user logged in:
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data = {
        id:"id"
    }
    current_user = user.User.get_one(data)
    return render_template('dashboard.html', current_user = current_user)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')