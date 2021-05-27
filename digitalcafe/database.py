import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
products_db = myclient["products"]
order_management_db = myclient["order_management"]

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code":code})
    
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]

    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)
    
    return product_list

def get_orders(username):
    orders_list = []
    orders_coll = order_management_db["orders"]
    orders_summary = orders_coll.find({"username":username},{"details":1})
    for u in orders_summary:
        for v in u["details"]:
            orders_list.append(v)

    return orders_list

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def get_password(username):
    customer_coll = order_management_db["customers"]
    password_dict = customer_coll.find_one({"username":username},{"password":1})
    password = password_dict['password']
    return password

def change_password(username,new_pass):
    customers_coll = order_management_db['customers']
    customers_coll.update_one({"username":username},{"$set":{"password":new_pass}})

def get_branch(code):
    branches_coll = products_db["branches"]
    branch_dict = branches_coll.find_one({"code":str(code)},{"name":1})

    return branch_dict

def get_branches():
    branch_list = []

    branches_coll = products_db["branches"]

    for b in branches_coll.find({},{"_id":0}):
        branch_list.append(b)

    return branch_list
