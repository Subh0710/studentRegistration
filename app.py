from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'abc*123/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger@123'
app.config['MYSQL_DB'] = 'studentdb'

mysql = MySQL(app)


@app.route('/')
def home_page():
    table = """select id,name,email,gender,mobile from register
               order by id desc
               Limit 10"""
    mysql.connection.commit()
    cursor = mysql.connection.cursor()
    cursor.execute(table)
    results = cursor.fetchall()
    cursor.close()
    return render_template('home.html', results=results)


@app.route('/add', methods=['POST', 'GET'])
def add():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        mobile = request.form['mobile']
        cursor = mysql.connection.cursor()
        result = cursor.execute('''INSERT INTO register (name,email,gender,mobile) VALUES (%s,%s,%s,%s)''',
                                (name, email, gender, mobile))
        mysql.connection.commit()
        flash('Data Inserted Successfully')
        cursor.close()
        return redirect(url_for('home_page'))
    return render_template('home.html', error=error)


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_no = request.form.get('id')
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        mobile = request.form.get('mobile')
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE register SET name=%s, email=%s, gender=%s, mobile=%s WHERE id=%s''', (name, email, gender, mobile, id_no))
        mysql.connection.commit()
        return redirect(url_for('home_page'))


@app.route('/delete/<string:id_no>', methods=['GET'])
def delete(id_no):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM register WHERE id=%s", (id_no))
    mysql.connection.commit()
    return redirect(url_for('home_page'))

if __name__ == '__main__':
    app.run()