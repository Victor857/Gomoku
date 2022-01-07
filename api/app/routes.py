from app import app, models
from flask import request, session
from app.game import Game
from app.models import PlayerRecord, GameRecord
from flask_login import current_user, login_user, logout_user
from jsonpickle import encode, decode

tiers =  ['Beginner', 'Intermediate', 'Experienced', 'Advanced', 'Ultimate']


@app.route('/api/settings', methods = ['POST'])
def apply_settings(): 
    settings = {}
    got = request.json 
    if got['colour'] == 'White':
        settings['computer'] = 0
    else:
        settings['computer'] = 2
    settings['difficulty'] = tiers.index(got['difficulty'])
    if current_user.is_anonymous:
        settings['playerID'] = 0
    else:
        settings['playerID'] = current_user.id
    session['game'] = encode(Game(settings))
    return {'':''}

@app.route('/api/checksettings')
def check_settings():
    res = str('game' in session)
    print(res)
    return {'res': res}

@app.route('/api/click', methods = ['POST'])
def click():
    game = decode(session['game'])
    ret = game.play_piece(request.json['index'])
    session['game'] = encode(game)
    return ret


@app.route('/api/board')
def get_board():
    print('get_board')
    return (decode(session['game']).get_board())


@app.route('/api/computer')
def cplay():
    game = decode(session['game'])
    ret = game.best_move()
    session['game'] = encode(game)
    return ret


@app.route('/api/history')
def history():
    if current_user.is_anonymous:
        return {'loggedin': False}
    return {'loggedin': True, 'games' : GameRecord.players_games(current_user.id)}


@app.route('/api/login', methods = ['POST'])
def login():
    got = request.json
    if not got['username']:
        return {'username':got['username'], 'pwd':got['pwd'], 'success': False, 
                'msg': 'Username cannot be empty'}
    if not got['pwd']:
        return {'username':got['username'], 'pwd':got['pwd'], 'success': False, 
                'msg': 'Password cannot be empty'}
    user = PlayerRecord.query.filter_by(username = got['username']).first()
    if user and user.check_pwd(got['pwd']):
        login_user(user)
        return {'success': True, 'link': session['link']}
    return {'username':got['username'], 'pwd':got['pwd'], 'success': False, 
                'msg': 'Username or password incorrect'}


@app.route('/api/signup', methods = ['POST'])
def signup():
    got = request.json
    err_msg = ''
    if not got['username']:
        err_msg = 'Username cannot be empty\n'
    elif PlayerRecord.query.filter_by(username = got['username']).first():
        err_msg = f"Username {got['username']} has already been taken by "\
                  + 'another user\n'
    elif not got['pwd']:
        err_msg = 'Password cannot be empty\n'
    elif not got['pwdConfirm'] or got['pwdConfirm'] != got['pwd']:
        err_msg = 'Password confirmation must match password'
    if err_msg:
        return {'username': got['username'], 'pwd': got['pwd'],
                'pwdConfirm': got['pwdConfirm'], 'success': False,
                'msg': err_msg}
    user = PlayerRecord(got['username'], '',got['pwd'])
    login_user(user)
    return {'success': True, 'link': session['link']} 


@app.route('/api/logout')
def logout():
    logout_user()
    return {'':''}


@app.route('/api/header')
def header():
    if current_user.is_anonymous:
        return {'loggedin': False}
    return {'loggedin': True, 'username': current_user.username}


@app.route('/api/storelink', methods = ['POST'])
def store_link():
    got = request.json
    session['link'] = got['link'] 
    return {'':''}

