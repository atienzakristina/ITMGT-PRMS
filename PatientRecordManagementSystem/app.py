from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import logging

app = Flask(__name__)

app.secret_key = b'w0w0w333111!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/tryagain')
def tryagain():
    return render_template('tryagain.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('availableservices.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/doctors')
def doctor():
    doctor_list = db.get_doctors()
    return render_template('doctors.html', doctor_list=doctor_list)

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/home')
    else:
        return redirect('/tryagain')

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect('/')
