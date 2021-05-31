import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

prms_db = myclient["PRMS"]

def get_user(username):
    patients_coll = prms_db['patients']
    patient=patients_coll.find_one({"username":username})
    return patient

doctors = {
    10 : {"firstname":"Ernesto","lastname":"Celdran","specialty":"X-Ray","time":{"6am":0,"7am":0,"8am":0,"9am":1,"10am":1,"11am":1,"12nn":1,"1pm":1,"2pm":1,"3pm":1,"4pm":1,"5pm":0,"6pm":0}},
    20 : {"firstname":"Maria","lastname":"Hechanova","specialty":"Blood Tests","time":{"6am":1,"7am":1,"8am":1,"9am":1,"10am":1,"11am":1,"12nn":1,"1pm":1,"2pm":0,"3pm":0,"4pm":0,"5pm":0,"6pm":0}},
    30 : {"firstname":"Salvador","lastname":"Perez","specialty":"CT Scan","time":{"6am":0,"7am":0,"8am":1,"9am":1,"10am":1,"11am":1,"12nn":1,"1pm":1,"2pm":1,"3pm":1,"4pm":1,"5pm":1,"6pm":1}},
    40 : {"firstname":"Teresa","lastname":"Galvez","specialty":"Ultrasound","time":{"6am":0,"7am":0,"8am":0,"9am":0,"10am":0,"11am":1,"12nn":1,"1pm":1,"2pm":1,"3pm":1,"4pm":1,"5pm":1,"6pm":1}},
    50 : {"firstname":"Timothy","lastname":"Recto","specialty":"Pulmonology","time":{"6am":0,"7am":1,"8am":1,"9am":1,"10am":1,"11am":1,"12nn":1,"1pm":0,"2pm":0,"3pm":0,"4pm":0,"5pm":0,"6pm":0}},
    60 : {"firstname":"Wilfredo","lastname":"Ongpin","specialty":"Molecular","time":{"6am":0,"7am":1,"8am":1,"9am":1,"10am":1,"11am":1,"12nn":1,"1pm":1,"2pm":1,"3pm":1,"4pm":1,"5pm":1,"6pm":0}}
    }

def get_doctor(code):
    return doctors[code]

def get_doctors():
    doctor_list = []

    for i,v in doctors.items():
        doctor = v
        doctor.setdefault("code",i)
        doctor_list.append(doctor)
    return doctor_list

def get_hours():
    for i,v in doctors:
        doctor = v
        doctor_hours = list(range(doctor["start_time"],doctor["end_time"]))
    return doctor_hours
