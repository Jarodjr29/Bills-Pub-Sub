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


class Config:
    """App configuration."""

    JOBS = [
        {
            "id": "pubWR_init",
            "func": "publish:pubWR",
            "args": (),
            "trigger": "date",
            "run_date": datetime.now() + timedelta(seconds=45),
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
        }
    ]

    SCHEDULER_API_ENABLED = True


def pubWR():
    week = 5
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'WR')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'WR': jdata})
    requests.post("http://web:5000/publish", data=jdic)

def pubRB():
    week = 5
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'RB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'RB': jdata})
    requests.post("http://web:5000/publish", data=jdic)

def pubQB():
    week = 5
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'QB')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'QB': jdata})
    requests.post("http://web:5000/publish", data=jdic)

def pubTE():
    week = 5
    data1 = nfl.import_rosters([2021])
    data1 = data1.loc[(data1['team'] == 'BUF') & (data1['status'] == 'Active') & (data1['position'] == 'TE')]
    data = nfl.import_weekly_data([2021])
    data = data.loc[(data['recent_team'] == 'BUF') & (data['week'] == week)]
    jdata = data.merge(data1, on="player_id")
    jdata = jdata.to_dict()
    jdic = json.dumps({'TE': jdata})
    requests.post("http://web:5000/publish", data=jdic)


def advertisewr():
    wr = {'wr': ['receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': wr}
    requests.post("http://web:5000/advertise", data=json.dumps(jdic))

def advertiseqb():
    qb = {'qb': ['completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'carries', 'rushing_Yards', 'rushing_tds']}
    jdic = {'stats': qb}
    requests.post("http://web:5000/advertise", data=json.dumps(jdic))


def advertisete():
    te = {'te': ['receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': te}
    requests.post("http://web:5000/advertise", data=json.dumps(jdic))


def advertiserb():
    rb = {'rb': ['carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds']}
    jdic = {'stats': rb}
    requests.post("http://web:5000/advertise", data=json.dumps(jdic))

def deadvertiser():
    jdic = {'msg': 'deadvertise'}
    requests.post("http://web:5000/deadvertise", data=json.dumps(jdic))

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
