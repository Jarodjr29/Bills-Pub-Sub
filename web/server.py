from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import flask_socketio
import mysql.connector
import json
from stmts import getStatements
import requests

app = Flask(__name__)
socketio = SocketIO(app)

def insert_reg(key, username, sid):
    mydb = mysql.connector.connect(
        host="webdb",
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
        host="webdb",
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
        host="webdb",
        user="root",
        password="pass"
    )
    cursor=mydb.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS messages")
    cursor.close()
    
    mydb = mysql.connector.connect(
        host="webdb",
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

@app.route("/notify", methods=['GET', 'POST'])
def notify():
    data = json.loads(request.data)
    topic = data['topic']
    socketio.emit("publish", data, room=topic)
    return 'notified'

@app.route("/joinRoom", methods=['GET', 'POST'])
def joinRoom():
    data = json.loads(request.data)
    socketio.emit('joined', data)
    print('hello', flush=True)
    return 'joined'

@socketio.on('joined')
def joined(data):
    print(data, flush=True)
    room = data['topic']
    sid = data['sid']
    join_room(room, sid)
    return "joined"



@socketio.on('register')
def subscribe(data):
    sid = request.sid
    data['sid'] = sid
    data = json.dumps(data)
    send(data)

def send(data):
    print("send", flush=True)
    requests.post('http://node4:5004/unsubscribe', data)
    requests.post('http://node4:5004/user', data)
    print("send", flush=True)

@socketio.on('unsubscribe')
def unsubscribe(data):
    requests.post()
    unsub(data, request.sid)
    leave_room(data['topic'])
    print(data)

def unsub(data1, sid):
    mydb = mysql.connector.connect(
        host="webdb",
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
    sid = request.sid
    data['sid'] = sid
    data = json.dumps(data)
    x = requests.post('http://node4:5004/subscribe', data)
    print(x.status_code, flush=True)

def sub(data1, sid):
    mydb = mysql.connector.connect(
        host="webdb",
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

@app.route("/advertise", methods=['GET', 'POST'])
def advertise():
    mydb = mysql.connector.connect(
        host="webdb",
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
    
@app.route("/publish", methods = ['GET', 'POST'])
def publish():
    data = json.loads(request.data)
    mydb = mysql.connector.connect(
        host="webdb",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    data = json.loads(request.data)
    key = data['key'].lower()
    data = data[key.upper()]
    stmts = getStatements(key)
    drop = "DROP TABLE IF EXISTS " + key
    cursor.execute(drop)
    create = stmts['create']
    cursor.execute(create)
    mydb.commit()
    cols = stmts['cols']
    num = len(data['season_x'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for k, v in obj.items():
            print(int(k))
            sql_list[int(k)].append(v)

    sql = [tuple(i,) for i in sql_list] 
    print(sql)
    insert = stmts['insert']
    cursor.executemany(insert, sql)
    mydb.commit()
    sql = "SELECT * FROM " + key
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    print(results)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, (key,))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'topic': key, 'data': results}
    if len(data)==0:
        print('fail')
    else:
        cursor.close()
        mydb.close()
        socketio.emit("publish", data2, room=key)
    return 'published'


@socketio.on('connection')
def connection():
    print("connection")

if __name__ == '__main__':
    initdb2()
    socketio.run(app, debug=True, port=5005, host='0.0.0.0')