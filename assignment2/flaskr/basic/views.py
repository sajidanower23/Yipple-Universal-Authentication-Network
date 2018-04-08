from flask import Flask, render_template_string, request, render_template, \
    redirect, url_for, session
from flask_session import Session

from . import app
from .. import models
import os
from .. import db

@app.route('/')
def home():
    username = None
    if 'username' in session:
        username = session['username']
    return render_template("home.html", username=username)

@app.route('/login', methods=["GET", "POST"])
def login():
    username = None
    password = None

    if request.method == "POST":
        # Implement me
        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')
        
        if username is not None and password is not None:

            succ, sess = models.validateUser(username, password)

            if succ is True:
                session['username'] = username
                # Craft the session
                return redirect('/')
            else:
                return "Login request failed", 400
        else:
            return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    username = None
    password = None
    result = False

    if request.method == "POST":
        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')

        if username is not None and password is not None:
            succ, status = models.registerUser(username, password)

            if succ is not False:
                return status, 200
            else:
                return status, 400
        return "User registration failed, either username or password is empty.", 400

    return render_template("register.html")

@app.route('/users/me', methods=["GET", "POST"])
def me():
    if 'username' not in session:
        return '403 permission denied', 403
    username = session['username']
    return users(username)

@app.route('/users/<account>', methods=["GET", "POST"])
def users(account):
    username = account # for consistency
    accessor = session['username']
    if username == 'admin' and not is_admin(accessor):
        return '403 permission denied', 403
    if request.method == 'GET':
        if has_access_own(accessor):
            user_info = get_user_info(username)
            response = render_template("users.html", username=username, user_info=user_info)
        else:
            response = "403 permission denied", 403
        # Deny access otherwise and display '404 not found' on the page
    elif request.method == 'POST':
        to_change_username = request.form.get('username')
        if is_admin(accessor) or to_change_username == accessor:# has_access_other(accessor):
            # TODO: Update The Credentials
            # Two types of users can edit credentials for <account>
            # 1. Regular Users that have sessions == <account>
            # 2. Administrators.
            update_creds(request.form)
            user_info = get_user_info(username)
            response = render_template("users.html", username=username, user_info=user_info)
        else:
            return '403 permission denied', 403

    return response

def get_user_info(username):
    uid = get_uid(username)
    if uid is None:
        return None
    (_, name, address, email, phone, funds) = \
        db.queryDB('SELECT * from creds where uid=?', (uid,), True)
    return {
        'name': name,
        'address': address,
        'email': email,
        'phone': phone,
        'funds': funds
    }

# Checks if user is logged in
def is_valid_user(username):
    if 'username' not in session: return False
    sess_username = session['username']
    return sess_username == username

def update_creds(new_creds):
    if 'username' in new_creds:
        user = new_creds['username'] # the one we are searching for
        name = new_creds['name']
        address = new_creds['address']
        email = new_creds['email']
        phonenum = new_creds['phonenum']
        funds = new_creds['funds']
        uid = get_uid(user)
        db.insertDB(
            'UPDATE creds SET name=?, address=?, email=?, \
            phonenum=?, funds=? WHERE uid=?', \
            (name, address, email, phonenum, funds, uid))


@app.route('/admin', methods=["GET", "POST"])
def admin():
    # why does admin.html have a login button?
    response = None
    # This is being checked in the function `is_admin`
    if 'username' not in session: return "403 permission denied"

    accessor = session['username']

    if not is_admin(accessor):
        return "403 permission denied", 403

    if request.method == 'GET':
        # TODO: Implement and secure the user administration control panel
        # The administration panel must distinguish between users that are administrators
        # as well as regular users.

        # It should also be able to search for a user via a get parameter called user.
        searchedUser = request.args.get('search')
        if searchedUser is not None: #if a user was searched for:

            user_info = get_user_info(searchedUser)
            if user_info is None:
                return '404 User not found', 404
            return render_template("admin.html", user=searchedUser, user_info=user_info)
        response = render_template("admin.html")

    elif request.method == 'POST':
        # TODO: You must also implement a post method in order update a searched users credentials.
        # It must return a page that denies a regular user
        # access and display '403 permission denied'.
        searchedUser = request.form.get('username')
        update_creds(request.form)
        user_info = get_user_info(searchedUser)
        return render_template("admin.html", user=searchedUser, user_info=user_info)

    return response

def has_access_own(username): return is_valid_user(username) or is_admin(username)
def has_access_other(username): return is_valid_user(username) and is_admin(username)

# Checks if user is admin
def is_admin(username):
    (isAdmin,) = db.queryDB('SELECT isAdmin from users where username=?', (username,), True)
    return isAdmin == 1 and is_valid_user(username)

def get_uid(username):
    # debug_log(username)
    (uid,) = db.queryDB('SELECT uid from users where username=?', (username,), True)    
    return uid


# Util function
def debug_log(msg):
    print('===================')
    print(msg)
    print('===================')
