__author__ = 'user'

from flask import *
from flaskext.mysql import MySQL
import MySQLdb
import uuid

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'april-23'
app.config['MYSQL_DATABASE_DB'] = 'estore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


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
            #usr = str(request.form['usrname'])
            usr = 'kganapathi'
            #pswrd = str(request.form['password'])
            pswrd = 'abc123'
            #email = str(request.form['email'])
            emailid = 'yokarthikg@gmail.com'
            #fname = str(request.form['fname'])
            fname = 'k'
            #lname = str(request.form['lname'])
            lname = 'gan'
            #gender = str(request.form['gender'])
            gender = 'M'
            #phone = str(request.form['Phone'])
            phone = 213452112
            customer_Id = 2
            cur = mysql.connect().cursor()
            #sql="""insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s)"""
            #cur.execute('insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s)',[customer_Id,usr,pswrd,email,fname,lname,gender,phone])
            query = """INSERT INTO estore.customer(Customer_Id, login_username, password, email, firstname, lastname, gender, phone_no) VALUES (str(customer_Id),"'"+usr+"'","'"+pswrd+"'","'"+emailid+"'","'"+fname+"'","'"+lname+"'","'"+gender+"'","'"+str(phone)+"'")"""
            cur.execute(query)
            mysql.connect().commit()
    return render_template("Registration.html", error=error)

@app.route('/View.html')
def view():
    return render_template("View.html")

@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("View.html",
        title = 'Home',
        user = user,
        posts = posts)



if __name__ == '__main__':
    app.run(debug=True)
