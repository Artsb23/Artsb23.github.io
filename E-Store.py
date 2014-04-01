from flask import *
import MySQLdb
import random
from flask_bootstrap import Bootstrap
import os
import datetime


app = Flask(__name__)

cnx = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'april-23',
    db = 'estore')
cur = cnx.cursor()

app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/Registration.html', methods=['GET', 'POST'])
def reg():
    error = ""
    if request.method == "POST":
        data = dict(request.form)
        if request.form["usrname"] == "" or request.form["password"] == "" or request.form["fname"] == "" or request.form["lname"] == "" or request.form["email"] == "":
            error = "Please fill in all the mandatory fields."
        else:
            usr = str(request.form['usrname'])
            #usr = 'kganapathi'
            pswrd = str(request.form['password'])
            #pswrd = 'abc123'
            email = str(request.form['email'])
            #email = 'yokarthikg@gmail.com'
            fname = str(request.form['fname'])
            #fname = 'k'
            lname = str(request.form['lname'])
            #lname = 'gan'
            gender = str(request.form['gender'])
            #gender = 'M'
            phone = str(request.form['Phone'])
            #phone = 213452112
            aptno = str(request.form['aptno'])
            Street = str(request.form['street'])
            City = str(request.form['city'])
            zip = str(request.form['zip'])
            state = str(request.form['state'])
            country = str(request.form['country'])
            cus_Id = check()
            session['cus_Id'] = cus_Id
            app.secret_key = os.urandom(24)


            query="INSERT INTO customer VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s')" % \
            (cus_Id,usr,pswrd,email,fname,lname,gender,phone)

            cur.execute(query)
            cur.execute("insert into address VALUES (%s, %s, '%s','%s', %s, '%s', '%s')" % (cus_Id,aptno,Street,City, zip, state, country))
            cnx.commit()
            return redirect(url_for('view', fname=fname, lname=lname))
    else:
        return render_template("Registration.html", error=error)

def check():
   customerId = random.getrandbits(8)
   check_id = cur.execute("select Customer_Id from customer where Customer_Id=%s" % (customerId))
   while check_id != 0:
       customerId = random.getrandbits(8)
       check_id = cur.execute("select Customer_Id from customer where Customer_Id=%s" % (customerId))
   return customerId

@app.route('/view?<fname>&<lname>', methods=['POST','GET'])
def view(fname, lname):
    if 'cus_Id' in session:
        error = None
        if request.method == 'POST':
            return redirect(url_for('shop',fname=fname))
        else:
            return render_template("View.html",fname=fname, lname=lname)
    else:
        error = "You are not logged in"
        render_template("login.html", error=error)

@app.route('/shop?<fname>')
def shop(fname):
    if 'cus_Id' in session:
        error = None
        img_list={}
        cur.execute("select distinct image, inv_name from inventory where Quantity > 0")
        result = cur.fetchall()
        for row in result:
            img_list[row[0]] = row[1]
        #img_list["fname"] = fname
        exist_cart = cur.execute("select Cart_Id, no_of_items from cart where customer_id = %s and Checkout = 0" % (session['cus_Id']))
        if exist_cart > 0:
            res = cur.fetchall()
            for rowno in res:
                cartId = rowno[0]
                items = rowno[1]
            return render_template('shop.html', img_list = img_list, fname=fname, items=items)
        else:
            return render_template('shop.html', img_list = img_list, fname=fname, items=0)
    else:
        error =  "You are not logged in"
        render_template("login.html", error=error)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        if request.form["usrname"] == "" or request.form["password"] == "":
            error = "Please fill in all the mandatory fields."
        else:

            usr = str(request.form['usrname'])
            pswrd = str(request.form['password'])
            confirm = cur.execute("select * from customer where login_username='%s' and password='%s'" % (usr,pswrd))

            if confirm > 0:
                results = cur.fetchall()
                for row in results:
                    fname = row[4]
                    cus_Id = row[0]
                session['cus_Id'] = cus_Id

                return redirect(url_for('shop', fname=fname))

            else:
                error = "Incorrect username and password "
                return render_template('login.html',error=error)

    else:
        return render_template('login.html')

@app.route('/dress?<name>/<path:image>', methods=['POST','GET'])
def dress(name, image):
    if 'cus_Id' in session:

            error = None
            inv_list = {}
            cur.execute("select distinct inv_size, color from inventory where inv_name = '%s' and Quantity > 0" % (name))
            try:
                result = cur.fetchall()

                for row in result:
                    if row[0] in inv_list:
                        inv_list[row[0]].append(row[1])
                    else:
                        inv_list[row[0]] = []
                        inv_list[row[0]].append(row[1])
                return render_template('Dress.html', name = name, image = image, inv_list = inv_list)
            except:
                error = "This inventory is not available"
                return render_template('Dress.html',error = error)
    else:
        error = "You are not logged in"
        return render_template('Dress.html',error = error)

@app.route('/add_to_cart')
def add_to_cart():

    if 'cus_Id' in session:
        error = None
        existing_cart = cur.execute("select Cart_Id, no_of_items from cart where customer_id = %s and Checkout = 0" % (session['cus_Id']))
        if existing_cart == 0:
            cartId = random.getrandbits(8)
            get_cartId = cur.execute("select * from cart where Cart_Id=%s" % (cartId))
            while get_cartId != 0:
                cartId = random.getrandbits(8)
                get_cartId = cur.execute("select * from cart where Cart_Id=%s" % (cartId))
            items = 0
            cart_exists = 0
        else:
            cart_exists = 1
            res = cur.fetchall()
            for row in res:
                cartId = row[0]
                items = row[1]
        items = items + 1
        coi_id = random.getrandbits(8)
        get_coi_id = cur.execute("select * from cart_inventory_info where Coi_id=%s" % (coi_id))
        while get_coi_id != 0:
            coi_id = random.getrandbits(8)
            get_coi_id = cur.execute("select * from cart_inventory_info where Coi_id=%s" % (coi_id))

        name = request.args.get('name')
        size = request.args.get('size')
        color = request.args.get('color')

        cur.execute("select Inventory_Id from inventory where inv_name = '%s' and inv_size = '%s' and color = '%s'" % (name, size, color))
        result = cur.fetchall()
        for row in result:
            inventory_id = row[0]
        try:
            if cart_exists == 1:
                cur.execute("update cart set no_of_items = %s where Cart_Id = %s and Customer_Id = %s" % (items, cartId, session['cus_Id']))

            else:
                cur.execute("insert into cart values(%s, %s, 0, %s)" % (cartId, session['cus_Id'], items))

            cart_inv = cur.execute("select * from cart_inventory_info where cart_id = %s and inventory_id = %s" % (cartId, inventory_id))
            if cart_inv == 1:
                cur.execute("update cart_inventory_info set Order_item_Qty = %s where Cart_Id = %s and Inventory_Id = %s" % (items, cartId, inventory_id))
            else:
                cur.execute("insert into cart_inventory_info values(%s,%s,%s,1)" % (coi_id, cartId, inventory_id))
            cnx.commit()
            return jsonify(result = items)
        except:
            cnx.rollback()

    else:
        error = "You are not logged in."
        render_template('login.html', error=error)

@app.route('/checkout', methods=["GET", "POST"])
def checkout():

    if 'cus_Id' in session:
        error = None
        res = cur.execute("select Cart_Id, no_of_items from cart where Customer_Id = %s and checkout = 0" % (session['cus_Id']))
        if res > 0:
            result1 = cur.fetchall()
            for row in result1:
                cartid = row[0]
                items = row[1]
            if items > 0:
                inventory_dict = {}
                cur.execute("select e.Inventory_Id, i.inv_name, i.inv_size, i.color, e.Order_item_Qty, i.cost, i.image, e.Coi_Id from cart_inventory_info e, inventory i where e.Inventory_Id = i.Inventory_Id and cart_id = %s" % (cartid))
                result2 = cur.fetchall()
                if request.method != "POST":
                    for row in result2:
                        if row[0] in inventory_dict:
                            inventory_dict[row[0]].append(row[1])
                            inventory_dict[row[0]].append(row[2])
                            inventory_dict[row[0]].append(row[3])
                            inventory_dict[row[0]].append(row[4])
                            inventory_dict[row[0]].append(row[5])
                            inventory_dict[row[0]].append(row[6])
                        else:
                            inventory_dict[row[0]] = []
                            inventory_dict[row[0]].append(row[1])
                            inventory_dict[row[0]].append(row[2])
                            inventory_dict[row[0]].append(row[3])
                            inventory_dict[row[0]].append(row[4])
                            inventory_dict[row[0]].append(row[5])
                            inventory_dict[row[0]].append(row[6])
                            print(inventory_dict)

                    return render_template("checkout.html", inventory_dict = inventory_dict)
                else:
                    orderId = random.getrandbits(8)
                    get_orderid = cur.execute("select * from orders where Order_Id=%s" % (orderId))
                    while get_orderid != 0:
                        orderId = random.getrandbits(8)
                        get_orderid = cur.execute("select * from orders where Order_Id=%s" % (orderId))
                    order_status = "Purchased"
                    order_date = datetime.datetime.now()
                    order_date = order_date.strftime('%Y/%m/%d %H:%M:%S')
                    order_cost = 0
                    Invoiceno = random.getrandbits(8)
                    get_Invoiceno = cur.execute("select * from invoice where invoice_no=%s" % (Invoiceno))
                    while get_Invoiceno != 0:
                        Invoiceno = random.getrandbits(8)
                        get_Invoiceno = cur.execute("select * from invoice where invoice_no=%s" % (Invoiceno))
                    Invoicedate = order_date
                    cur.execute("select e.Inventory_Id, i.inv_name, i.inv_size, i.color, e.Order_item_Qty, i.cost, i.image, e.Coi_Id from cart_inventory_info e, inventory i where e.Inventory_Id = i.Inventory_Id and cart_id = %s" % (cartid))
                    results = cur.fetchall()
                    for row in results:
                        order_cost += (int(row[4]) * int(row[5]))
                    try:
                        cur.execute("insert into orders values (%s, '%s', '%s', %s)" % (orderId, order_status, order_date, order_cost))
                        cur.execute("insert into invoice values (%s, %s, '%s')" % (Invoiceno,orderId, Invoicedate))
                        for row in result2:
                            inv_id = row[0]
                            coi_id = row[7]
                            qty = row[4]
                            orderitemId = random.getrandbits(8)
                            get_orderitemid = cur.execute("select * from order_items where Order_Item_Id=%s" % (orderitemId))
                            while get_orderitemid != 0:
                                orderitemId = random.getrandbits(8)
                                get_orderitemid = cur.execute("select * from order_items where Order_Item_Id=%s" % (orderitemId))
                            shipmentid = random.getrandbits(8)
                            get_shipmentid = cur.execute("select * from shipment where Shipment_Id=%s" % (shipmentid))
                            while get_shipmentid != 0:
                                shipmentid = random.getrandbits(8)
                                get_shipmentid = cur.execute("select * from shipment where Shipment_Id=%s" % (shipmentid))
                            trackingid = random.getrandbits(16)
                            get_trackingid = cur.execute("select * from shipment where Shipment_Tracking_No=%s" % (trackingid))
                            while get_trackingid != 0:
                                trackingid = random.getrandbits(8)
                                get_trackingid = cur.execute("select * from shipment where Shipment_Tracking_No=%s" % (trackingid))
                            Shipment_date = order_date
                            cur.execute("insert into order_items values (%s, %s, %s, %s)" % (orderitemId, orderId, inv_id, coi_id))
                            cur.execute("insert into shipment values (%s, %s, %s, '%s')" % (shipmentid, orderitemId, trackingid, Shipment_date))
                            cur.execute("update cart set checkout = 1 where cart_id = %s" % (cartid))
                            cur.execute("update inventory set Quantity = Quantity - %s where Inventory_Id = %s" % (qty, inv_id))
                            cnx.commit()
                        return render_template("order.html", orderId = orderId, order_status = order_status, order_date = order_date, order_cost = order_cost )
                    except:
                        cnx.rollback()
                        return "Transaction Failure"

            else:
                cur.execute("select fname from customer where customer_id = %s" % (session['cus_Id']))
                r = cur.fetchall()
                for row in r:
                    fname = row[0]
                return redirect(url_for("shop", fname=fname))

        else:
            cur.execute("select firstname from customer where customer_id = %s" % (session['cus_Id']))
            r = cur.fetchall()
            for row in r:
                fname = row[0]
            return redirect(url_for("shop", fname=fname))


    else:
        error = "Session timed out. You are not logged in"
        return render_template("login.html", error=error)


@app.route('/template_header')
def template_header():
    if 'cus_Id' in session:
        error = None
        existing_cart = cur.execute("select no_of_items from cart where customer_id = %s and Checkout = 0" % (session['cus_Id']))
        if existing_cart > 0:
            result = cur.fetchall()
            for row in result:
                items = row[0]

            return jsonify(result = items)
        else:
            return jsonify(result = 0)
    else:

        return jsonify(result = 0)

if __name__ == '__main__':
    app.run(debug=True)

