from app import db, login
from datetime import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class GameRecord(db.Model):
    def __init__(self, playerID, side, difficulty, res, plays):
        self.playerID = playerID
        self.side = side
        self.difficulty = difficulty
        self.result = res
        self.plays = "".join([chr(n) for n in plays])
        self.time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer)
    side = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    result = db.Column(db.Integer)
    plays = db.Column(db.String(225))
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def details(self):
        return {'id': self.id, 'playerID': self.playerID, 'side':self.side, 
                'difficulty': self.difficulty, 'result': self.result, 
                'plays': [ord(c) for c in self.plays], 'time': self.time}

    def __repr__(self):
        return f'{self.details()}'

    @staticmethod
    def commitdb():
        db.session.commit()
    
    @staticmethod
    def all_games():
        return list(map(GameRecord.details, GameRecord.query.all()))[1:]

    @staticmethod
    def players_games(ID):
        return list(map(GameRecord.details, GameRecord.query.filter_by(playerID=ID)))


class PlayerRecord(UserMixin, db.Model):
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd_hash = generate_password_hash(pwd)
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(254))
    pwd_hash = db.Column(db.String(128))

    def details(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def __repr__(self):
        return f'{self.details()}'

    @staticmethod
    def recordPlayer(player):
        p = PlayerRecord(player)
        print(p)
        db.session.add(p)
        db.session.commit()


@login.user_loader
def load_user(id):
    return PlayerRecord.query.get(int(id))


