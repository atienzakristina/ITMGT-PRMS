import database as db

def login(username, password):
    is_valid_login = False
    user=None
    temp_user = db.get_doctor_account(username)
    if(temp_user != None):
        if(temp_user["password"]==password):
            is_valid_login=True
            doctor={"username":username,
                  "firstname":temp_user["firstname"],
                  "lastname":temp_user["lastname"]}

    return is_valid_login, doctor
