from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import logging
import numpy as np

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

@app.route('/myappointments')
def myappointments():
    username = session["user"]["username"]
    appointments_list = db.get_appointments(username)

    return render_template('myappointments.html',appointments_list=appointments_list)

@app.route('/booking')
def booking():
    services_list = db.get_services()
    return render_template('booking.html', services_list=services_list)

@app.route('/date', methods = ['GET','POST'])
def date():
    code = request.args.get('code', '')
    doctor = db.get_doctor(int(code))
    return render_template('date.html',code=code, doctor=doctor)


@app.route('/schedule', methods = ['GET','POST'])
def appointment():
    date = request.form.get('date')
    code = request.form.get('code')
    doctor = db.get_doctor(int(code))
    doctor_schedule = db.get_schedule(int(code))
    doctor_range = list(np.arange(doctor_schedule["start_time"],doctor_schedule["end_time"],0.5))
    doctor_hours = []

    for x in doctor_range:
        if x % 1 > 0:
            y = str(x)
            z = y.replace(".5",":30")
            doctor_hours.append(z)
        else:
            y = str(x)
            z = y.replace(".0",":00")
            doctor_hours.append(z)
    doctor_available_hours = []
    for y in doctor_hours:
        if len(db.existing_appointments(str(code),date,y)) == 0:
            doctor_available_hours.append(y)
        else:
            pass

    return render_template('appointmentbooking.html', doctor=doctor,date=date, code=code, doctor_available_hours=doctor_available_hours)

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
