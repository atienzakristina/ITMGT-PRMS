import database as db
from flask import session
from datetime import datetime

def confirm_appointment(code,timeslot,date):
    appointment = {}
    appointment.setdefault("username",session["user"]["username"])
    appointment.setdefault("bookingdate",datetime.utcnow())
    appointment.setdefault("code",code)
    appointment.setdefault("timeslot",timeslot)
    appointment.setdefault("date",date)
    db.create_appointment(appointment)
