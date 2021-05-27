import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

prms_db = myclient["PRMS"]

def get_user(username):
    patients_coll = prms_db['patients']
    patient=patients_coll.find_one({"username":username})
    return patient

doctors = {
    10 : {"firstname":"Ernesto","lastname":"Celdran","specialty":"X-Ray","start_time":10,"end_time":17},
    20 : {"firstname":"Maria","lastname":"Hechanova","specialty":"Blood Tests","start_time":8,"end_time":13},
    30 : {"firstname":"Salvador","lastname":"Perez","specialty":"CT Scan","start_time":11,"end_time":19},
    40 : {"firstname":"Teresa","lastname":"Galvez","specialty":"Ultrasound","start_time":7,"end_time":13},
    50 : {"firstname":"Timothy","lastname":"Recto","specialty":"Pulmonology","start_time":9,"end_time":18},
    60 : {"firstname":"Wilfredo","lastname":"Ongpin","specialty":"Molecular","start_time":12,"end_time":13}
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
