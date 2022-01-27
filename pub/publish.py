from datetime import datetime, timedelta
import os
import sys
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import pickle
import json
import requests
from flask_apscheduler import APScheduler
import nfl_data_py as nfl
import pandas as pd
from requests.api import get


class Config:
    """App configuration."""

    JOBS = [
        {
            "id": "pubWR_init",
            "func": "publish:pubWR",
            "args": (),
            "trigger": "date",
            "run_date": (datetime.now() + timedelta(seconds=15)),
        },{
            "id": "pubQB",
            "func": "publish:pubQB",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=55),
        },{
            "id": "pubTE",
            "func": "publish:pubTE",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=65),
        },{
            "id": "pubRB",
            "func": "publish:pubRB",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=75),
        },{
            "id": "advertisewr",
            "func": "publish:advertisewr",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=30),
        },{
            "id": "advertiseqb",
            "func": "publish:advertiseqb",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=30),
        },{
            "id": "advertisete",
            "func": "publish:advertisete",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=30),
        },{
            "id": "advertiserb",
            "func": "publish:advertiserb",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=30),
        },{
            "id": "deadvertiser",
            "func": "publish:deadvertiser",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=60),
        },{
            "id": "pubOppWR",
            "func": "publish:pubOppWR",
            "args": (),
            "trigger": "date",
            "run_date": (datetime.now() + timedelta(seconds=15)),
        },{
            "id": "puboppQB",
            "func": "publish:pubOppQB",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=55),
        },{
            "id": "pubOppTE",
            "func": "publish:pubOppTE",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=65),
        },{
            "id": "pubOppRB",
            "func": "publish:pubOppRB",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=75),
        },{
            "id": "pubRoster",
            "func": "publish:pubRoster",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=55),
        },{
            "id": "pubSched",
            "func": "publish:pubSched",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=65),
        },{
            "id": "pubOpponent",
            "func": "publish:pubOpponent",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=75),
        },{
            "id": "pubOpponentRoster",
            "func": "publish:pubOpponentRoster",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=75),
        }
    ]

    SCHEDULER_API_ENABLED = True


def pubWR():
    week = nfl.import_weekly_data([2021])['week'].max() - 1 
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'WR')] 
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'WR': jdata, 'key': 'WR'})
    requests.post("http://node1:5001/publish", data=jdic)

def pubRB():
    week = nfl.import_weekly_data([2021])['week'].max() - 1 
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'RB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'RB': jdata, 'key': 'rb'})
    requests.post("http://node1:5001/publish", data=jdic)

def pubQB():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'QB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'QB': jdata, 'key': 'qb'})
    requests.post("http://node1:5001/publish", data=jdic)

def pubTE():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'TE')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'TE': jdata, 'key': 'te'})
    requests.post("http://node1:5001/publish", data=jdic)

def pubRoster():
    roster = nfl.import_rosters([2021])
    team_roster = roster.loc((roster['team'] == 'BUF') & (roster['status'] == 'Active'))
    jdata = team_roster.to_dict()
    jdic = json.dumps({'roster': jdata, 'key': 'roster'})
    requests.post("http://node2:5002/publish", data=jdic)

def pubSched():    
    data = nfl.import_schedules([2021])
    sched = data.loc[(data['home_team'] == 'BUF') | (data['away_team'] == 'BUF')]
    jdata = sched.to_dict()
    jdic = json.dumps({'schedule': jdata})
    requests.post("http://node2:5002/publish", data=jdic)

def pubOpponent():
    week = nfl.import_weekly_data([2021])['week'].max() 
    data = nfl.import_schedules([2021])
    info = data.loc[(data['week'] == week) & ((data['home_team'] == 'BUF') | (data['away_team'] == 'BUF'))]
    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    jdic = json.dumps({'opponent': opp, 'key': 'opponent'})
    requests.post("http://node3:5003/publish", data=jdic)

def pubOpponentRoster():
    week = nfl.import_weekly_data([2021])['week'].max() 
    data = nfl.import_schedules([2021])
    roster = nfl.import_rosters([2021])

    info = data.loc[(data['week'] == week) & ((data['home_team'] == 'BUF') | (data['away_team'] == 'BUF'))]

    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    team_roster = roster.loc(roster['team'] == opp & roster['status'] == 'Active')
    jdata = team_roster.to_dict()
    jdic = json.dumps({'roster': jdata, 'key': 'oppRoster'})
    requests.post("http://node3:5003/publish", data=jdic)

def pubOppWR():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    data1 = data1.loc[(data1['team'] == opp) & (data1['status'] == 'Active') & (data1['position'] == 'WR')] 
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == opp) & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'OPPWR': jdata, 'key': 'OPPWR'})
    requests.post("http://node4:5004/publish", data=jdic)

def pubOppRB():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    data1 = data1.loc[(data1['team'] == opp) & (data1['status'] == 'Active') & (data1['position'] == 'RB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == opp) & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'OPPRB': jdata, 'key': 'opprb'})
    requests.post("http://node4:5004/publish", data=jdic)

def pubOppQB():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    data1 = data1.loc[(data1['team'] == opp) & (data1['status'] == 'Active') & (data1['position'] == 'QB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == opp) & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'OPPQB': jdata, 'key': 'oppqb'})
    requests.post("http://node4:5004/publish", data=jdic)

def pubOppTE():
    week = nfl.import_weekly_data([2021])['week'].max() - 1
    data1 = nfl.import_rosters([2021])
    opponent = getOpponent()
    opp = ''
    for val in opponent.values():
        opp = val
    data1 = data1.loc[(data1['team'] == opp) & (data1['status'] == 'Active') & (data1['position'] == 'TE')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == opp) & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'OPPTE': jdata, 'key': 'oppte'})
    requests.post("http://node4:5004/publish", data=jdic)

def getOpponent():
    week = nfl.import_weekly_data([2021])['week'].max()
    data = nfl.import_schedules([2021])

    info = data.loc[(data['week'] == week) & ((data['home_team'] == 'BUF') | (data['away_team'] == 'BUF'))]
    info = info.to_dict()
    opponent = info['home_team']
    if info['home_team'] == 'BUF':
        opponent = info['away_team']
    else:
        opponent = info['home_team']
    return opponent

def advertisewr():
    wr = {'wr': ['receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': wr}
    requests.post("http://web:5005/advertise", data=json.dumps(jdic))

def advertiseqb():
    qb = {'qb': ['completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'carries', 'rushing_Yards', 'rushing_tds']}
    jdic = {'stats': qb}
    requests.post("http://web:5005/advertise", data=json.dumps(jdic))


def advertisete():
    te = {'te': ['receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': te}
    requests.post("http://web:5005/advertise", data=json.dumps(jdic))


def advertiserb():
    rb = {'rb': ['carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': rb}
    requests.post("http://web:5005/advertise", data=json.dumps(jdic))

def deadvertiser():
    jdic = {'msg': 'deadvertise'}
    requests.post("http://web:5005/deadvertise", data=json.dumps(jdic))

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
