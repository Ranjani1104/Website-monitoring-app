from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))
    status = db.Column(db.Integer)
    latency = db.Column(db.Float)
    is_up = db.Column(db.Boolean)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)