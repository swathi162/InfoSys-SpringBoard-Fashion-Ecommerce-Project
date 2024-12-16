from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# to be changed as per the ER Diagram Provided by the team
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
