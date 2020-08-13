import os


class Config:
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    # os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
