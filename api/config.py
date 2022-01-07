import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'aospneojtnypsbazo'
    SECRET_KEY = os.environ.get('SECRET_KEY', '80d03ab359084e3abbd54918b79bde89')
    SESSION_TYPE = 'filesystem'
