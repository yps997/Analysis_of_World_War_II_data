class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1234@localhost:5437/missions_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True