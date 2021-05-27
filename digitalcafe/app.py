from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes
# keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/orders')
def orders():
    username = session["user"]["username"]
    order_list = db.get_orders(username)

    return render_template('viewpastorders.html', page="View Past Orders", order_list=order_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(code)

    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/try_again', methods=['GET', 'POST'])
def try_again():
    return render_template('tryagain.html')

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    return render_template('changepassword.html')

@app.route('/change', methods=['GET', 'POST'])
def change():
    username = request.form.get('username')
    old_pass = request.form.get('old_password')
    new_pass = request.form.get('new_password')
    new_pass2 = request.form.get('new_password2')

    check_old_pass = db.get_password(username)

    if check_old_pass == old_pass:
        if new_pass == new_pass2:
            db.change_password(username,new_pass)
            session.pop("user",None)
            return redirect('/login')
        else:
            return redirect('/changepassword')
    else:
        return redirect('/changepassword')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/try_again')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')


@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    # A click to add a product translates to a
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/changeqty', methods = ['POST'])
def changeqty():
    cart = session["cart"]
    code = request.form.get('code')
    qty = int(request.form.get("qty"))
    
    product = db.get_product(int(code))

    if qty == 0:
        del cart[code]
    else:
        cart[code]["qty"] = qty
        cart[code]["subtotal"] = qty * product["price"]
        session["cart"] = cart
    
    session['cart'] = cart
    

    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/api/products',methods=['GET'])
def api_get_products():
    resp = make_response( dumps(db.get_products()) )
    resp.mimetype = 'application/json'
    return resp

@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.get_product(code)))
    resp.mimetype = 'application/json'
    return resp
