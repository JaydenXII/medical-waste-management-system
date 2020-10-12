from app import bcrypt, db
from app.models import Staff, Waste, Vehicle
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

def GetAvailableVehicle():
    vehicle_list = []
    vehicles = Vehicle.query.filter_by(available=True).all()
    for v in vehicles:
        vehicle_list.append(v.id)
    return vehicle_list

class LoginForm(FlaskForm):
    id = StringField("Staff ID", validators=[DataRequired(), Length(min=1, max=6)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)])
    rememberme = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class QRCodeForm(FlaskForm):
    qrcode = MultipleFileField("QRCode", validators=[
        FileRequired(),
        FileAllowed(["jpg", "heic", "png"], "Format isn't supported")
    ])
    send_vehicle = SelectField("Select Vehicle", choices=GetAvailableVehicle())
    submit = SubmitField("Confirm")

class RegisterForm(FlaskForm):
    type = StringField("Waste Type", validators=[DataRequired()])
    submit = SubmitField("Confirm")

class UserSetting(FlaskForm):
    name = StringField("Name", validators=[Length(max=20)])
    password = StringField("Password", validators=[Length(max=16)])
    confirm_password = StringField("Confirm Password", validators=[Length(max=16), EqualTo("password")])
    phone = StringField("Phone", validators=[Length(max=15)])
    submit = SubmitField("Confirm")

class AdminLoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=20)])
    page = SelectField("Select Page", choices=[("staff", "Add Staff"), ("vehicle", "Add Vehicle")])
    submit = SubmitField("Confirm")

class AdminStaffForm(FlaskForm):
    id = IntegerField("Staff ID")
    name = StringField("Name", validators=[Length(max=20)])
    password = StringField("Password (if staff exists)", validators=[Length(max=16)])
    confirm_password = StringField("Confirm Password (if staff exists)", validators=[Length(max=16), EqualTo("password")])
    phone = StringField("Phone", validators=[Length(max=15)])
    submit = SubmitField("Confirm")

class AdminVehicleField(FlaskForm):
    id = StringField("Vehicle ID", validators=[DataRequired(), Length(max=8)])
    driver = StringField("Driver", validators=[Length(max=20)])
    waste_type = StringField("Waste Type", validators=[Length(max=1)])
    submit = SubmitField("Confirm")