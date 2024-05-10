from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_session import Session  # Session management
from flask_cors import CORS
import openai
import os

application = Flask(__name__)
CORS(application)
application.config['SECRET_KEY'] = 'a_secret_key_you_should_change'  # Change this to a random secret key
application.config['SESSION_TYPE'] = 'filesystem'  # Can be 'redis', 'memcached', 'filesystem', 'mongodb', etc.
Session(application)

# Dummy user database (usually you will use a database system)
users = {"admin": "password123"}  # Username and password

@application.route('/')
def home():
    if 'username' in session:
        return render_template('submit_essay.html')  # Only logged-in users can see the essay submission page
    return redirect(url_for('login'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')  # Display the login form

@application.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Other routes (fetch-issue, submit-essay) stay unchanged
# Ensure these routes check for 'username' in session to enforce login

if __name__ == '__main__':
    application.run(debug=True)
