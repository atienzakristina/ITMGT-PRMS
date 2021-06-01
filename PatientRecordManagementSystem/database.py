import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

prms_db = myclient["PRMS"]

def get_user(username):
    patients_coll = prms_db['patients']
    patient=patients_coll.find_one({"username":username})
    return patient

doctors = {
    10 : {"username":"ernesto@doctors.com","password":"qwerty","firstname":"Ernesto","lastname":"Celdran","specialty":"X-Ray","time":{"start_time":9,"end_time":17}},
    20 : {"username":"maria@doctors.com","password":"qwerty","firstname":"Maria","lastname":"Hechanova","specialty":"Blood Tests","time":{"start_time":8,"end_time":13}},
    30 : {"username":"salvador@doctors.com","password":"qwerty","firstname":"Salvador","lastname":"Perez","specialty":"CT Scan","time":{"start_time":11,"end_time":18}},
    40 : {"username":"teresa@doctors.com","password":"qwerty","firstname":"Teresa","lastname":"Galvez","specialty":"Ultrasound","time":{"start_time":10,"end_time":16}},
    50 : {"username":"timothy@doctors.com","password":"qwerty","firstname":"Timothy","lastname":"Recto","specialty":"Pulmonology","time":{"start_time":7,"end_time":12}},
    60 : {"username":"wilfredo@doctors.com","password":"qwerty","firstname":"Wilfredo","lastname":"Ongpin","specialty":"Molecular","time":{"start_time":12,"end_time":18}}
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

def get_services():
    services_list = []
    for i,v in doctors.items():
        services_list.append(dict([("code",i)]))
        services_list.append(dict([("specialty",v["specialty"])]))
    return services_list

def get_schedule(code):
    doctor = doctors[code]
    doctor_schedule = doctor[time]
    doctor_hours = list(range(doctor_schedule["start_time"],doctor_schedule["end_time"]))

    return doctor_hours
