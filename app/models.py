from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Staff.query.filter_by(id=id).first()

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    waste = db.relationship("Waste", backref=db.backref("collector", lazy=True), lazy=True)

    def __repr__(self):
        return f"<Staff {self.id}>"

class Waste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(5), nullable=False)
    collect_time = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id")) 
    is_sent = db.Column(db.Boolean, default=False, nullable=False)
    send_time = db.Column(db.DateTime)
    vehicle_id = db.Column(db.String(10), db.ForeignKey("vehicle.id"))

    def __repr__(self):
        return f"<Waste {self.id}>"

class Vehicle(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    driver = db.Column(db.String(20), nullable=False)
    waste_type = db.Column(db.String(5), nullable=False)
    available = db.Column(db.Boolean, default=False, nullable=False)
    waste = db.relationship("Waste", backref=db.backref("carrier", lazy=True), lazy=True)

    def __repr__(self):
        return f"<Vehicle {self.id}>"