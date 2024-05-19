from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    transcript = db.Column(db.Text, nullable=False)
