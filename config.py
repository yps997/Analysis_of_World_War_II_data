class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/missions_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True