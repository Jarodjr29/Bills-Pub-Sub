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
from stmts import getStatements
import requests
app = Flask(__name__)
socketio = SocketIO(app)

def insert_reg(key, username, sid):
    mydb = mysql.connector.connect(
        host="node4db",
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
    else:
        stmt = "UPDATE users SET " + key + " = 1 WHERE username = %s"
        cursor.execute(stmt, (username,))
        stmt = "SELECT * FROM users WHERE username = (%s)"
        cursor.execute(stmt, (username,))
        data= cursor.fetchall()
        print(data)
        data2 = {'data': data}
    mydb.commit()
    cursor.close()
    mydb.close()

def loginDB(data, sid):
    mydb = mysql.connector.connect(
        host="node4db",
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
        host="node4db",
        user="root",
        password="pass"
    )
    cursor=mydb.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS messages")
    cursor.close()
    
    mydb = mysql.connector.connect(
        host="node4db",
        user="root",
        password="pass",
        database="messages"
    )
    users = getStatements('users4')
    cursor=mydb.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS sids (sid TEXT, username TEXT)")
    cursor.execute(users['create'])
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


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    data = json.loads(request.data)
    sid = data['sid']
    username = data['username']
    for key in data.keys():
        if data[key] == '1':
            node = routing(key)
            if node == 'node4':
                insert_reg(key, username, sid)
            else:
                send = "http://" + node + ":500" + node[-1] + "/register"
                requests.post(send, json.dumps(data))

@app.route('/reg', methods=['GET', 'POST'])
def register():
    data = json.loads(request.data)
    sid = data['sid']
    username = data['username']
    for key in data.keys():
        if data[key] == '1':
            node = routing(key)
            if node == 'node4':
                insert_reg(key, username, sid)
            else:
                send = "http://" + node + ":500" + node[-1] + "/register"
                data = {'username': username, 'sid': sid, key: '1'}
                requests.post(send, json.dumps(data))
    return('registered')

@app.route('/unsubscribe', methods = ['GET', 'POST'])
def unsubscribe():
    data = json.loads(request.data)
    sid = data['sid']
    username = data['username']
    su = {'sid': sid, 'username': username}
    requests.post('http://node4:5004/user', json.dumps(su))
    for key in data.keys():
        print(key, flush=True)
        if data[key] == '1':
            node = routing(key)
            if node == 'node4':
                insert_reg(key, username, sid)
            else:
                print('hello', flush=True)
                send = "http://" + node + ":500" + node[-1] + "/unsubscribe"
                sd = {'username': username, 'sid': sid, key: '1'}
                requests.post(send, json.dumps(sd))
    return('registered')

def unsub(data1, sid):
    mydb = mysql.connector.connect(
        host="node4db",
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

@app.route('/subscribe', methods = ['GET', 'POST'])
def subscribe():
    data = json.loads(request.data)
    node = routing(data['topic'])
    if node == 'node4':
        sub(data, data['sid'])
        return 'sub'
    else:
        send = "http://" + node + ":500" + node[-1] + "/subscribe"
        requests.post(send, request.data)
        return 'routed'

def sub(data1, sid):
    mydb = mysql.connector.connect(
        host="node4db",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    stmt = "SELECT * FROM sids WHERE sid = %s"
    cursor.execute(stmt, (sid,))
    data= cursor.fetchall()
    username = data[0][1]
    topic = data1['topic']
    stmt = "SELECT username FROM users WHERE username = %s"
    cursor.execute(stmt, (username, ))
    data = cursor.fetchall()
    if len(data) == 0:
        stmt = "INSERT INTO users(username, " + topic + ") VALUES (%s, 1)"
        cursor.execute(stmt, (username,))
    else:
        stmt = "UPDATE users SET " + topic + " = 1 WHERE username = %s"
        cursor.execute(stmt, (username,))
    mydb.commit()
    cursor.close()
    mydb.close()
    data = json.dumps({'topic': topic, 'sid': sid})
    print("subbing", flush=True)
    requests.post('http://web:5005/joinRoom', data)
    return 'subbed'

@socketio.on('login')
def login(data):
    loginDB(data, request.sid)
    print(data)
    
@app.route("/user", methods=['GET', 'POST'])
def user():
    data = json.loads(request.data)
    sid = data['sid']
    username = data['username']
    mydb = mysql.connector.connect(
        host="node4db",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    stmt = "SELECT * FROM sids WHERE username = %s"
    cursor.execute(stmt, (username,))
    exists = cursor.fetchall()
    if len(exists) == 0:
        stmt = "INSERT INTO sids (sid, username) VALUES (%s, %s)"
        cursor.execute(stmt, (sid, username, ))
    else:
        stmt = "UPDATE sids SET sid = %s WHERE username = %s" 
        cursor.execute(stmt, (sid, username,))
    requests.post('http://node3:5003/user', json.dumps(data))
    mydb.commit()
    cursor.close()
    mydb.close()
    return 'user'

@app.route("/advertise", methods=['GET', 'POST'])
def advertise():
    mydb = mysql.connector.connect(
        host="node4db",
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
        host="node4db",
        user="root",
        password="pass",
        database="messages"
    )
    cursor = mydb.cursor()
    key = data['key'].lower()
    node = routing(key)
    if node != 'node4':
        requests.post("http://" + node + ":500" + node[-1] + "/publish", data=request.data)
    data = data[key.upper()]
    stmts = getStatements(key)
    drop = "DROP TABLE IF EXISTS " + key
    cursor.execute(drop)
    create = stmts['create']
    cursor.execute(create)
    mydb.commit()
    cols = stmts['cols']
    num = len(data['week'].keys())
    sql_list = [[i] for i in range(0,num)]
    for col in cols:
        obj = data[col]
        for k, v in obj.items():
            sql_list[int(k)].append(v)

    sql = [tuple(i,) for i in sql_list] 
    insert = stmts['insert']
    cursor.executemany(insert, sql)
    mydb.commit()
    sql = "SELECT * FROM " + key
    cursor.execute(sql)
    results = cursor.fetchall()
    cols.insert(0, 'index')
    results.insert(0, cols)
    stmt = "SELECT room FROM rooms WHERE room = (%s)"
    cursor.execute(stmt, (key,))
    data= cursor.fetchall()
    cursor.close()
    mydb.close()
    data2 = {'topic': key, 'data': results}
    requests.post('http://web:5005/notify', json.dumps(data2))
    return 'published'

@socketio.on('connection')
def connection():
    print("connection")

def routing(topic):
    nodes = {
    'wr': 'node1',
    'rb': 'node1',
    'qb': 'node1',
    'te': 'node1',
    'roster': 'node2',
    'schedule': 'node2',
    'opponent': 'node3',
    'opproster': 'node3',
    'oppwr': 'node4',
    'opprb': 'node4',
    'oppqb': 'node4',
    'oppte': 'node4',
    }
    if nodes[topic] == 'node4':
        return('node4')
    else: 
        #stmt = "SELECT connection FROM connections WHERE node = (%s)"
        #cursor.execute(stmt, ('node4',))
        #cur = cursor.fetchall()
        #connections = cur[1]
        if int(nodes[topic][-1]) < 4:
            return('node3')
        #else:
        #    node = "node4"
        #    for x in range(3, 4 - 1):
        #        if connections[x] == 1:
        #            node = "node" + x
                        



if __name__ == '__main__':
    socketio.run(app, port=5004, host='0.0.0.0', debug=True)