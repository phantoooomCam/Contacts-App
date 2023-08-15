from flask import Flask, render_template, request,url_for,redirect,flash
from flask_mysqldb import MySQL

app = Flask(__name__)


#mysql connection
app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"]= "password"
app.config["MYSQL_DB"] = "flask-contacts"
mysql= MySQL(app)

#session settings
app.secret_key='mysecretkey'



@app.route('/')
def Index():
    cur =mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html',contacts = data)

@app.route('/contact',methods=['POST'])
def add_Contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',(fullname,phone,email))
        mysql.connection.commit()
        flash('Contact Added Succesfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_Contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',[id])
    data = cur.fetchall()
    return render_template('edit.html', contact=data[0])
    
@app.route('/update/<string:id>',methods=['POST'])
def update_Contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts 
            SET fullname = %s,
                    email =%s,
                    phone = %s
            WHERE id = %s
            """, (fullname,email,phone,id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_Contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Succesfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)

