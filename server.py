import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import mysql.connector
import json

app = Flask(__name__)


    
@app.route("/")
def index():
    return redirect(url_for('initdb'))

@app.route("/home")
def home():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM inputs")
    
    messages = cursor.fetchall()
    
    mydb.close()
    return render_template('index.html', messages=messages)

@app.route("/input", methods=['GET', 'POST'])
def message():
    print(list(request.form['message']))
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = request.form['message']
    print(data)
    stmt = "INSERT INTO inputs (input) VALUES (%s)"
    cursor.execute(stmt, (data,))
    mydb.commit()
    cursor.close()
    mydb.close()
    
    return redirect(url_for('home'))

@app.route("/initdb")
def initdb():    
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass"
    )
    cursor=mydb.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS messages")
    cursor.close()
    
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    
    cursor=mydb.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS inputs (input VARCHAR(255))")
    cursor.close()
    
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')