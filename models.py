from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    passwd = db.Column(db.String(50))
    
    # name Type
    # email Type
    # password Type