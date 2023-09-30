from flask import Flask, render_template, request, redirect,  url_for, session
import mysql.connector
import re
from plot_graph import plot_graph
from passlib.context import CryptContext


app = Flask(__name__)

app.secret_key = 'c@s3D3vG0l'

db = mysql.connector.connect(
    host="localhost",
    user="gol",
    password="d3vG0l",
    database="analytics_gol"
)

context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(buffered=True)
        query1 = 'SELECT id, username, name, last_login, create_user, password FROM user WHERE username = "{}"'.format(username)
        cursor.execute(query1)
        user = cursor.fetchone()
        
        if user and (user[5] == password or context.verify(password, user[5])):
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            msg = 'Logged in successfully !'
            query2 = 'UPDATE user SET last_login = NOW() WHERE username = "{}"'.format(username)
            cursor.execute(query2)
            db.commit()
            return render_template('index.html', msg=msg, user=user)
            
        else:
            msg = 'Incorrect username / password !'
            
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    if 'loggedin' in session:
	    session.pop('loggedin', None)
	    session.pop('id', None)
	    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/")
def index():
    if 'loggedin' in session:
        cursor = db.cursor(buffered=True)
        query1 = 'SELECT * FROM user WHERE id = {}'.format(session['id'])
        cursor.execute(query1)
        user = cursor.fetchone()
        return render_template("index.html", user=user)
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = db.cursor(buffered=True)
        query1 = 'SELECT * FROM user WHERE id = {}'.format(session['id'])
        cursor.execute(query1)
        user = cursor.fetchone()
        return render_template("display.html", user=user)
    return redirect(url_for('login'))


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    
    msg = ''

    if request.method == 'POST': 
        if 'username' in request.form and 'password' in request.form and 'name' in request.form:
    
            username = request.form['username']
            password = request.form['password']
            password = context.hash(password)
            name = request.form['name']
            cursor = db.cursor(buffered=True)
            query1 = 'SELECT * FROM user WHERE username = "{}"'.format(username)
            cursor.execute(query1)
            user = cursor.fetchone()
            
            if user:
                msg = 'Account already exists !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                query2 = 'INSERT INTO user (username, password, name, create_user) VALUES \
                    ("{}", "{}", "{}", NOW());'.format(username, password, name)
                cursor.execute(query2)
                db.commit()
                msg = 'You have successfully registered !'
                return redirect(url_for('login.html'))
            
        else:
            msg = 'Please fill out the form !'
        
    return render_template('register.html', msg=msg)


@app.route("/user/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            
            if 'username' in request.form or 'password' in request.form or 'name' in request.form:
                username = request.form['username']
                password = request.form['password']
                if password:
                    password = context.hash(password)
                name = request.form['name']
                cursor = db.cursor(buffered=True)
                query1 = 'SELECT * FROM user WHERE id = {}'.format((session['id']))
                cursor.execute(query1)
                user = cursor.fetchone()
                if not(user):
                    msg = 'Usuário não existe !'
                if username:
                    query2 = 'SELECT * FROM user WHERE username = "{}" and id != {}'.format(username, (session['id']))
                    cursor.execute(query2)
                    user_username = cursor.fetchone()
                    print(user_username)
                    print(session['id'])

                    if not(user_username):

                        if not re.match(r'[A-Za-z0-9]+', username):
                            msg = 'Não é permitido character especial, nome deve conter apenas letras e numeros !'
                        elif password and name:
                            query3 ='UPDATE user SET username = "{}", password = "{}", name = "{}" WHERE id = {}'.format(username, password, name,(session['id']))
                            cursor.execute(query3)
                            db.commit()
                            msg = 'You have successfully updated !'
                        elif password and not(name):
                            query3 ='UPDATE user SET username = "{}", password = "{}" WHERE id = {}'.format(username, password, (session['id']))
                            cursor.execute(query3)
                            db.commit()
                            msg = 'You have successfully updated !'
                        elif not(password) and (name):
                            query3 ='UPDATE user SET username = "{}", name = "{}" WHERE id = {}'.format(username, name,(session['id']))
                            cursor.execute(query3)
                            db.commit()
                            msg = 'You have successfully updated !'
                        else:
                            query3 ='UPDATE user SET username = "{}" WHERE id = {}'.format(username,(session['id']))
                            cursor.execute(query3)
                            db.commit()
                            msg = 'You have successfully updated !'
                    else:
                        msg = 'Usuário já utilizado'
                    
                elif password and not(name):
                    query3 ='UPDATE user SET password = "{}" WHERE id = {}'.format(password, (session['id']))
                    cursor.execute(query3)
                    db.commit()
                    msg = 'You have successfully updated !'
                elif not(password) and (name):
                    query3 ='UPDATE user SET name = "{}" WHERE id = {}'.format(name,(session['id']))
                    cursor.execute(query3)
                    db.commit()
                    msg = 'You have successfully updated !'
        
            else:
                msg = 'Adicionar algum dado para atualização !'
                
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))

@app.route("/analytics/search", methods=['GET', 'POST'])
def search():
    msg = ''

    if 'loggedin' in session:
        cursor = db.cursor(buffered=True)
        if request.method == 'GET':
            query1 = 'SELECT DISTINCT market from analytic_data'
            cursor.execute(query1)
            market_list = cursor.fetchall()
            return render_template('search.html', market_list=market_list)
        elif request.method == 'POST':
            if 'date_year_begin' in request.form and 'date_month_begin' in request.form and 'date_year_end' in request.form and 'date_month_end' in request.form and 'market' in request.form:
                date_year_begin = request.form['date_year_begin']
                date_month_begin = request.form['date_month_begin']
                date_year_end = request.form['date_year_end']
                date_month_end = request.form['date_month_end']
                market = request.form['market']
                query2 = 'SELECT * FROM analytic_data \
                WHERE market = "{}" and date_year >= {} and date_year <= {} \
                and date_month >= {} and date_month <= {}'.format(market,date_year_begin,date_year_end,date_month_begin,date_month_end)
                cursor.execute(query2)
                data_list = cursor.fetchall()
                query3 = 'INSERT INTO log_query (user_id, log_timestamp, market, year_begin, month_begin, year_end, month_end) VALUES \
                ({}, NOW(), "{}", {}, {}, {}, {})'.format((session['id']), market, date_year_begin, date_month_begin, date_year_end, date_month_end)
                cursor.execute(query3)
                db.commit()
                query4 = 'SELECT LAST_INSERT_ID() FROM log_query'
                cursor.execute(query4)
                log_id = cursor.fetchone()
                for log in data_list:
                    query5 = 'INSERT INTO log_analytic (log_id, analytic_id) VALUES ({}, {})'.format(log_id[0], log[0])
                    cursor.execute(query5)
                    db.commit()
                
                plot_graph(data_list)
                return redirect('result.html')
                
            else:
                msg = 'Please fill out the form !'
                query1 = 'SELECT DISTINCT market from analytic_data'
                cursor.execute(query1)
                market_list = cursor.fetchall()
                return render_template('search.html', msg=msg, market_list=market_list)

    return redirect(url_for('login'))

@app.route('/analytics/result')
def result():
    pathfile =  'static/images/rpk_por_data.png'
    return render_template("result.html", graph_result = pathfile)

@app.route("/analytics/log")
def log():
    if 'loggedin' in session:
        cursor = db.cursor(buffered=True)
        query1 = 'SELECT * FROM log_query WHERE user_id = {}'.format(session['id'])
        cursor.execute(query1)
        log_user = cursor.fetchall()
        return render_template("log.html", log_user=log_user)
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run()
