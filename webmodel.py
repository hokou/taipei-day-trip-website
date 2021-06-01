from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# print(dir(db))

class Attraction(db.Model):
    __tablename__ = 'attraction_data'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    rowid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.VARCHAR(255), nullable=False)
    category = db.Column(db.VARCHAR(255), nullable=True)
    description = db.Column(db.VARCHAR(2000), nullable=True)
    address = db.Column(db.VARCHAR(255), nullable=True)
    transport = db.Column(db.VARCHAR(2000), nullable=True)
    mrt = db.Column(db.VARCHAR(2000), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    images = db.Column(db.VARCHAR(4000), nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, rowid, name, category, description, address, transport, mrt, latitude, longitude, images):
        self.rowid = rowid
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.latitude = latitude
        self.longitude = longitude
        self.images = images

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password