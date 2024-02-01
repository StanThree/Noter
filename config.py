# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://tristan:thethousand@localhost/noterdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    DEBUG = False