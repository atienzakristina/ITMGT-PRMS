import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

prms_db = myclient["PRMS"]

def get_user(username):
    patients_coll = prms_db['patients']
    patient=patients_coll.find_one({"username":username})
    return patient

def get_doctor_account(username):
    doctors_coll = prms_db['doctors']
    doctor=doctors_coll.find_one({"username":username})
    return doctor

def get_doctor(code):
    doctors_coll = prms_db['doctors']
    doctor = doctors_coll.find_one({"code":code})

    return doctor

def get_doctors():
    doctor_list = []
    doctors_coll = prms_db['doctors']

    for v in doctors_coll.find({},{"_id":0}):
        doctor_list.append(v)
    return doctor_list

def get_services():
    services_list = []
    services_coll = prms_db['doctors']
    for v in services_coll.find({},{"_id":0}):
        services_list.append(v)
    return services_list

def get_schedule(code):
    doctors_coll = prms_db['doctors']
    doctor_sched = doctors_coll.find_one({"code":code})
    doctor_hours = doctor_sched["time"]

    return doctor_hours

def create_appointment(appointment):
    appointments_coll = prms_db['appointments']
    appointments_coll.insert(appointment)

def existing_appointments(code,date,timeslot):
    appointments_list = []
    appointments_coll = prms_db['appointments']
    for a in appointments_coll.find({"code":code,"date":date,"timeslot":timeslot}):
        appointments_list.append(a)

    return appointments_list

def get_appointments(username):
    appointments_list = []
    appointments_coll = prms_db['appointments']
    doctors_coll = prms_db['doctors']

    for a in appointments_coll.find({"username":username}):
        code = a["code"]
        doctor = doctors_coll.find_one({"code":int(code)})
        appointments_list.append({"date":a["date"],
                                  "timeslot":a["timeslot"],
                                  "status":a["status"],
                                  "specialty":doctor["specialty"],
                                  "firstname":doctor["firstname"],
                                  "lastname":doctor["lastname"],
                                  })
    return appointments_list

def pending_appointments(code):
    pending_list = []
    appointments_coll = prms_db['appointments']
    patients_coll = prms_db['patients']

    for a in appointments_coll.find({"code":str(code),"status":"Pending"}):
        patient_user = a["username"]
        patient = patients_coll.find_one({"username":patient_user})
        pending_list.append({"firstname":patient["firstname"],
                             "lastname":patient["lastname"],
                             "code":a["code"],
                             "date":a["date"],
                             "timeslot":a["timeslot"],
                             "status":a["status"],
                             })
    return pending_list

def accept_appointment(code,date,timeslot):
    appointment_coll = prms_db['appointments']
    appointment = appointment_coll.update_one({"code":str(code),"date":date,"timeslot":timeslot},{"$set":{"status":"Accepted"}})

def reject_appointment(code,date,timeslot):
    appointment_coll = prms_db['appointments']
    appointment = appointment_coll.update_one({"code":str(code),"date":date,"timeslot":timeslot},{"$set":{"status":"Rejected"}})

def accepted_appointments(code):
    accepted_list = []
    appointments_coll = prms_db['appointments']
    patients_coll = prms_db['patients']

    for a in appointments_coll.find({"code":str(code),"status":"Accepted"}):
        patient_user = a["username"]
        patient = patients_coll.find_one({"username":patient_user})
        accepted_list.append({"firstname":patient["firstname"],
                              "lastname":patient["lastname"],
                              "date":a["date"],
                              "timeslot":a["timeslot"],
                              "status":a["status"],
                             })
    return accepted_list

def create_account(username,password,firstname,lastname,age):
    patients_coll = prms_db['patients']
    patients_coll.insert({"username":username,"password":password,"firstname":firstname,"lastname":lastname,"age":int(age)})
