import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

prms_db = myclient["PRMS"]

def get_user(username):
    patients_coll = prms_db['patients']
    patient=patients_coll.find_one({"username":username})
    return patient

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
