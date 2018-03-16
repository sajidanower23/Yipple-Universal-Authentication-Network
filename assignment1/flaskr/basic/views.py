from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Implement me
        username = models.sanitise_name(request.form.get('username'))
        password = request.form.get('password')
        is_valid = models.validateUser(username, password)
        if is_valid:
            session['username'] = username
            return redirect(
                        url_for('basic.users',
                        account=username))
        else:
            return "Invalid credentials", 403

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Implement me
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            if models.registerUser(username, password):
                return redirect(url_for('basic.login'))
            else:
                return "User already exists", 400
        except:
            return "Could not process request", 500
    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    # Implement me
    return render_template("users.html", account=account)
