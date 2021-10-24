from functools import singledispatch
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import mysql.connector
import json
import pickle

app = Flask(__name__)
socketio = SocketIO(app)

def insert_reg(key, username, sid):
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    stmt = "INSERT INTO rooms (room) VALUES (%s)"
    cursor.execute(stmt, (key,))
    mydb.commit()
    stmt = "INSERT INTO sids (sid, username) VALUES (%s, %s)"
    cursor.execute(stmt, (sid, username, ))
    stmt = "SELECT * FROM users WHERE username = (%s)"
    cursor.execute(stmt, (username,))
    data= cursor.fetchall()
    if len(data) == 0:
        stmt = "INSERT INTO users (username, " + key + ") VALUES (%s, '1')"
        cursor.execute(stmt, (username,))
        stmt = "SELECT * FROM users WHERE username = (%s)"
        cursor.execute(stmt, (username,))
        data= cursor.fetchall()
        print(data)
        data2 = {'data': data}
        socketio.emit('joined', data2, room=sid)
    else:
        stmt = "UPDATE users SET " + key + " = 1 WHERE username = %s"
        cursor.execute(stmt, (username,))
        stmt = "SELECT * FROM users WHERE username = (%s)"
        cursor.execute(stmt, (username,))
        data= cursor.fetchall()
        print(data)
        data2 = {'data': data}
        socketio.emit('joined', data2, room=sid)
    mydb.commit()
    cursor.close()
    mydb.close()

def loginDB(data, sid):
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    username = data['username']
    stmt = "UPDATE sids SET sid = %s WHERE username = %s"
    cursor = mydb.cursor()
    cursor.execute(stmt, (sid, username,))
    stmt = "SELECT * FROM users WHERE username = (%s)"
    cursor.execute(stmt, (username,))
    datau= cursor.fetchall()
    print(datau)
    cols = ['username', 'wr', 'rb', 'qb', 'te']
    data2 = {'data': datau}
    socketio.emit('joined', data2, room=sid)
    for i in range(1, len(cols)):
        stmt = "SELECT * FROM users WHERE username = (%s)"
        cursor.execute(stmt, (username,))
        datau= cursor.fetchall()
        print(datau)
        data2 = {'data': datau[0][i]}
        datal = {'len': len(datau)}
        socketio.emit('joined', data2, room=sid)
        socketio.emit('joined', datal, room=sid)
        if datau[0][i] == '1':
            socketio.emit('joined', {'sub': cols[i]}, room=sid)
            join_room(cols[i], sid)
    mydb.commit()
    cursor.close()
    mydb.close()

@app.before_request
def initdb2():    
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
    users = '''CREATE TABLE IF NOT EXISTS users(
        username CHAR(25) PRIMARY KEY,
        wr CHAR(5),
        rb CHAR(5),
        qb CHAR(5),
        te CHAR(5)
        )'''
    cursor=mydb.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS sids (sid TEXT, username TEXT)")
    cursor.execute(users)
    cursor.execute("CREATE TABLE IF NOT EXISTS rooms (room TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS subjects (topics TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS wrSubs (input TEXT,  input2 TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rbSubs (input TEXT,  input2 TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS qbSubs (input TEXT,  input2 TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS teSubs (input TEXT,  input2 TEXT)")
    cursor.close()
    mydb.commit()
    mydb.close()

    
@app.route("/")
def index():
    return render_template("signup.html")

@socketio.on('register')
def register(data):
    sid = request.sid
    print(data)
    username = data['username']
    subs = []
    for key in data.keys():
        if data[key] == '1':
            join_room(key)
            insert_reg(key, username, request.sid)
    print(username)

@socketio.on('unsubscribe')
def unsubscribe(data):
    unsub(data, request.sid)
    leave_room(data['topic'])
    print(data)

def unsub(data1, sid):
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    stmt = "SELECT * FROM sids WHERE sid = %s"
    cursor.execute(stmt, (sid,))
    data= cursor.fetchall()
    username = data[1][1]
    topic = data1['topic']
    stmt = "UPDATE users SET " + topic + " =  0 WHERE username = %s"
    cursor.execute(stmt, (username,))
    mydb.commit()
    cursor.close()
    mydb.close()

@socketio.on('subscribe')
def subscribe(data):
    sub(data, request.sid)
    join_room(data['topic'])
    print(data, request.sid)

def sub(data1, sid):
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    stmt = "SELECT * FROM sids WHERE sid = %s"
    cursor.execute(stmt, (sid,))
    data= cursor.fetchall()
    username = data[1][1]
    topic = data1['topic']
    stmt = "UPDATE users SET " + topic + " = 1 WHERE username = %s"
    cursor.execute(stmt, (username,))
    mydb.commit()
    cursor.close()
    mydb.close()

@socketio.on('login')
def login(data):
    loginDB(data, request.sid)
    print(data)
    

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    data = request.form['username']
    data2 = request.form['wr']
    data3 = request.form['qb']
    data4 = request.form['rb']
    message = [data, data2, data3, data4]
    return render_template("index.html", messages=message)

@app.route("/advertise", methods=['GET', 'POST'])
def advertise():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    data = json.loads(request.data)
    stats = data['stats']
    topic = ""
    for key in stats.keys():
        topic = key
    data = {'topic': topic, 'data': stats}
    socketio.emit('advert', data)
    return 'advertised'

@app.route("/deadvertise", methods=['GET', 'POST'])
def deadvertise():
    data = json.loads(request.data)
    socketio.emit("deadvertise", data)
    return 'deadvertised'

@app.route("/WR", methods = ['GET', 'POST'])
def WR():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = json.loads(request.data)
    data = data['WR']
    cursor.execute("DROP TABLE IF EXISTS wr")
    stmt = '''CREATE TABLE IF NOT EXISTS wr(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )'''
    cursor.execute(stmt)
    mydb.commit()
    cols = ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds']
    num = len(data['targets'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for key, val in obj.items():
            print(int(key))
            sql_list[int(key)].append(val)

    sql = [tuple(i,) for i in sql_list] 
    print(sql)
    stmt = "INSERT INTO wr (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(stmt, sql)
    mydb.commit()
    sql = "SELECT * FROM wr"
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    print(results)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, ('wr',))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'topic': 'wr', 'data': results}
    if len(data)==0:
        print('fail')
    else:
        cursor.close()
        mydb.close()
        socketio.emit("publish", data2, room='wr')
    return 'published'

@app.route("/QB", methods = ['GET', 'POST'])
def QB():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = json.loads(request.data)
    data = data['QB']
    cursor.execute("DROP TABLE IF EXISTS qb")
    stmt = '''CREATE TABLE IF NOT EXISTS qb(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        completions INT,
        attempts INT,
        passing_yards INT,
        passing_tds INT,
        interceptions INT,
        carries INT,
        rushing_yards INT,
        rushing_tds INT
        )'''
    cursor.execute(stmt)
    mydb.commit()
    cols = ['week', 'player_name_x', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'carries', 'rushing_yards', 'rushing_tds']
    num = len(data['completions'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for key, val in obj.items():
            print(int(key))
            sql_list[int(key)].append(val)

    sql = [tuple(i,) for i in sql_list] 
    print(sql)
    stmt = "INSERT INTO qb (spot, week, player_name_x, completions, attempts, passing_yards, passing_tds, interceptions, carries, rushing_yards, rushing_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(stmt, sql)
    mydb.commit()
    sql = "SELECT * FROM qb"
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    print(results)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, ('qb',))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'data': results, 'topic': 'qb'}
    if len(data)==0:
        print('fail')
    else:
        cursor.close()
        mydb.close()
        socketio.emit("publish", data2, room='qb')
    return 'published'

@app.route("/RB", methods = ['GET', 'POST'])
def RB():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = json.loads(request.data)
    data = data['RB']
    cursor.execute("DROP TABLE IF EXISTS rb")
    stmt = '''CREATE TABLE IF NOT EXISTS rb(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        carries INT,
        rushing_yards INT,
        rushing_tds INT,
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )'''
    cursor.execute(stmt)
    mydb.commit()
    cols = ['week', 'player_name_x', 'carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds']
    num = len(data['completions'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for key, val in obj.items():
            print(int(key))
            sql_list[int(key)].append(val)

    sql = [tuple(i,) for i in sql_list] 
    print(sql)
    stmt = "INSERT INTO rb (spot, week, player_name_x, carries, rushing_yards, rushing_tds, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(stmt, sql)
    mydb.commit()
    sql = "SELECT * FROM rb"
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    print(results)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, ('rb',))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'topic': 'rb', 'data': results}
    if len(data)==0:
        print('fail')
    else:
        cursor.close()
        mydb.close()
        socketio.emit("publish", data2, room='rb')
    return 'published'

@app.route("/TE", methods = ['GET', 'POST'])
def TE():
    mydb = mysql.connector.connect(
        host="msgdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = json.loads(request.data)
    data = data['TE']
    cursor.execute("DROP TABLE IF EXISTS te")
    stmt = '''CREATE TABLE IF NOT EXISTS te(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )'''
    cursor.execute(stmt)
    mydb.commit()
    cols = ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds']
    num = len(data['targets'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for key, val in obj.items():
            print(int(key))
            sql_list[int(key)].append(val)

    sql = [tuple(i,) for i in sql_list] 
    print(sql)
    stmt = "INSERT INTO te (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(stmt, sql)
    mydb.commit()
    sql = "SELECT * FROM te"
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    print(results)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, ('te',))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'topic': 'te', 'data': results}
    if len(data)==0:
        print('fail')
    else:
        cursor.close()
        mydb.close()
        socketio.emit("publish", data2, room='te')
    return 'published'

@app.route("/publish", methods = ['GET', 'POST'])
def publish():
    data = json.loads(request.data)
    url = ""
    for key in data.keys():
        url = key
    return redirect(url_for(url), code=307)

@socketio.on('connection')
def connection():
    print("connection")

if __name__ == '__main__':
    initdb2()
    socketio.run(app, debug=True, host='0.0.0.0')