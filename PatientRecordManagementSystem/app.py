from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import logging

import appointmentmanagement as am

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
    services_list = db.get_services()
    return render_template('booking.html', services_list=services_list)

@app.route('/schedule', methods = ['GET','POST'])
def appointment():
    code = request.args.get('code', '')
    doctor_schedule = db.get_schedule(int(code))
    doctor_hours = list(range(doctor_schedule["start_time"],doctor_schedule["end_time"]))

    return render_template('appointmentbooking.html', code=code, doctor_hours=doctor_hours)

@app.route('/confirmation', methods = ['GET','POST'])
def confirmation():
    code = request.form.get('code')
    doctor = db.get_doctor(int(code))
    timeslot = request.form.get('timeslot')
    date = request.form.get('date')

    return render_template('confirmbooking.html', date=date, doctor=doctor,code=code,timeslot=timeslot)


@app.route('/confirm', methods = ['GET', 'POST'])
def confirm():
    code = request.form.get('code')
    timeslot = request.form.get('timeslot')
    date = request.form.get('date')
    am.confirm_appointment(code,timeslot,date)
    return redirect('/bookingconfirmed')

@app.route('/bookingconfirmed')
def ordercomplete():
    return render_template('bookingcomplete.html')

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
