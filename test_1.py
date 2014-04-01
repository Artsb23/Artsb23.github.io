import MySQLdb

cnx = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'april-23',
    db = 'estore')
cur = cnx.cursor()
#usr = str(request.form['usrname'])
usr = 'kganapathi'
#pswrd = str(request.form['password'])
pswrd = 'abc123'
#email = str(request.form['email'])
email = 'yokarthikg@gmail.com'
#fname = str(request.form['fname'])
fname = 'k'
#lname = str(request.form['lname'])
lname = 'gan'
#gender = str(request.form['gender'])
gender = 'M'
#phone = str(request.form['Phone'])
phone = 213452112
customer_Id = 4


#query = "insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s)",(customer_Id,usr,pswrd,email,fname,lname,gender,phone)
query="INSERT INTO customer VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s')" % \
       (customer_Id,usr,pswrd,email,fname,lname,gender,phone)

cur.execute(query)
cnx.commit()

