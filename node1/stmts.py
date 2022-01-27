

stmts = {
    'receiving': {
        'create': '''CREATE TABLE IF NOT EXISTS receiving(
        spot INT PRIMARY KEY,
        position CHAR(5),
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )''',
        'cols': ['week', 'position', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO wr (spot, position, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    },
    'rushing': {
        'create': '''CREATE TABLE IF NOT EXISTS rushing(
        spot INT PRIMARY KEY,
        position CHAR(5),
        week INT,
        player_name_x CHAR(25),
        carries INT,
        rushing_yards INT,
        rushing_tds INT,
        )''',
        'cols': ['week', 'position', 'player_name_x', 'carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO rb (spot, position, week, player_name_x, carries, rushing_yards, rushing_tds, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    },
    'qb': {
        'create': '''CREATE TABLE IF NOT EXISTS qb(
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
        )''',
        'cols': ['week', 'player_name_x', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'carries', 'rushing_yards', 'rushing_tds'],
        'insert': "INSERT INTO qb (spot, week, player_name_x, completions, attempts, passing_yards, passing_tds, interceptions, carries, rushing_yards, rushing_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    },
    'rb': {
        'create': '''CREATE TABLE IF NOT EXISTS rb(
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
        )''',
        'cols': ['week', 'player_name_x', 'carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO rb (spot, week, player_name_x, carries, rushing_yards, rushing_tds, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    },
    'wr': {
        'create': '''CREATE TABLE IF NOT EXISTS wr(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )''',
        'cols': ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO wr (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    },
    'te': {
        'create': '''CREATE TABLE IF NOT EXISTS te(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )''',
        'cols': ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO te (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    },
    'roster': {
        'create': '''CREATE TABLE IF NOT EXISTS roster(
        player_name CHAR(50) PRIMARY KEY,
        position CHAR(10),
        jersey_numer INT
        )''',
        'cols': ['[player_name', 'position', 'jersey_number'],
        'insert': 'INSERT INTO roster (player_name, position, jersey_number) VALUES (%s, %s, %s)'
    },
    'schedule': {
        'create': '''CREATE TABLE IF NOT EXISTS schedule(
        season INT,
        week INT,
        home_team CHAR(10),
        away_team CHAR(10)
        )''',
        'cols': ['season', 'week', 'home_team', 'away_team'],
        'insert': 'INSERT INTO schedule (season, week, home_team, away_team) VALUES (%s, %s, %s, %s)'
    },
    'opproster': {
        'create': '''CREATE TABLE IF NOT EXISTS oppRoster(
        player_name CHAR(50) PRIMARY KEY,
        position CHAR(10),
        jersey_numer INT
        )''',
        'cols': ['player_name', 'position', 'jersey_number'],
        'insert': 'INSERT INTO oppRoster (player_name, position, jersey_number) VALUES (%s, %s, %s)'
    },
    'opponent': {
        'create': '''CREATE TABLE IF NOT EXISTS opponent(
        name CHAR(25),
        week INT
        )''',
        'cols': ['name', 'week'],
        'insert': 'INSERT INTO opponent (name, week) VALUES (%s, %s)'
    },
    'oppqb': {
        'create': '''CREATE TABLE IF NOT EXISTS qb(
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
        )''',
        'cols': ['week', 'player_name_x', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'carries', 'rushing_yards', 'rushing_tds'],
        'insert': "INSERT INTO qb (spot, week, player_name_x, completions, attempts, passing_yards, passing_tds, interceptions, carries, rushing_yards, rushing_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    },
    'opprb': {
        'create': '''CREATE TABLE IF NOT EXISTS rb(
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
        )''',
        'cols': ['week', 'player_name_x', 'carries', 'rushing_yards', 'rushing_tds', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO rb (spot, week, player_name_x, carries, rushing_yards, rushing_tds, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    },
    'oppwr': {
        'create': '''CREATE TABLE IF NOT EXISTS wr(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )''',
        'cols': ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO wr (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    },
    'oppte': {
        'create': '''CREATE TABLE IF NOT EXISTS te(
        spot INT PRIMARY KEY,
        week INT,
        player_name_x CHAR(25),
        receptions INT,
        targets INT,
        receiving_yards INT,
        receiving_tds INT
        )''',
        'cols': ['week', 'player_name_x', 'receptions', 'targets', 'receiving_yards', 'receiving_tds'],
        'insert': "INSERT INTO te (spot, week, player_name_x, receptions, targets, receiving_yards, receiving_tds) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    },
    'nodes': {
    'wr': 'node1',
    'rb': 'node1',
    'qb': 'node1',
    'te': 'node1',
    'receiving': 'node1',
    'passing': 'node1',
    'rushing': 'node1',
    'roster': 'node2',
    'schedule': 'node2',
    'opponent': 'node3',
    'opproster': 'node3',
    'oppwr': 'node4',
    'opprb': 'node4',
    'oppqb': 'node4',
    'oppte': 'node4',
    },
    'users1': {'create': '''CREATE TABLE IF NOT EXISTS users(
        username CHAR(25) PRIMARY KEY,
        wr CHAR(5),
        rb CHAR(5),
        qb CHAR(5),
        te CHAR(5)
        )'''
    },
    'users2': {'create': '''CREATE TABLE IF NOT EXISTS users(
        username CHAR(25) PRIMARY KEY,
        roster CHAR(5),
        sched CHAR(5)
        )'''
    },
    'users3': {'create': '''CREATE TABLE IF NOT EXISTS users(
        username CHAR(25) PRIMARY KEY,
        opponent CHAR(5),
        opproster CHAR(5)
        )'''
    },
    'users4': {'create': '''CREATE TABLE IF NOT EXISTS users(
        username CHAR(25) PRIMARY KEY,
        oppwr CHAR(5),
        opprb CHAR(5),
        oppqb CHAR(5),
        oppte CHAR(5),
        )'''
    }

}

def getStatements(key):
    return stmts[key]