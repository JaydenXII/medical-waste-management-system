from app import app, bcrypt, db
from app.forms import *
from app.imgfunc import *
from app.models import Staff, Waste, Vehicle
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from os.path import join
from werkzeug.utils import secure_filename
 
@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(id=form.id.data).first()
        if staff and bcrypt.check_password_hash(staff.password, form.password.data):
            login_user(staff, remember=form.rememberme.data)
            flash("Login successfully", category="success")
            return redirect(url_for("scan"))
        flash("User doesn't exist or password not match", category="danger")
    return render_template("login.html", form=form)

@app.route("/scan")
@login_required
def scan():
    form = QRCodeForm()
    return render_template("scan.html", form=form)

@app.route("/scan", methods=["POST"])
@login_required
def upload_qrcode():
    if request.method == "POST":
        if "qrcode" not in request.files:
            flash("No file part", category="danger")
            return redirect(url_for("scan"))
        qrcodes = request.files.getlist("qrcode")
        vehicle = Vehicle.query.filter_by(id=request.form.get("vehicle_id")).first()
        if vehicle and vehicle.available == True:
            time = datetime.now()
            for qrcode in qrcodes:
                if allowed_file(qrcode.filename):
                    filename = secure_filename(qrcode.filename)
                    path = join(app.config["TEMP_UPLOAD_DIRECTORY"], filename)
                    qrcode.save(path)
                    result = Waste.query.filter_by(id=QrDec(path)).first()
                    if result and result.is_sent == False:
                        if result.type == vehicle.waste_type:
                            result.is_sent = True
                            db.session.commit()
                            flash(f"Waste {result.id} is sent.", category="success")
                        else:
                            flash("The type of waste is not allowed on this vehicle.", category="danger")
                    else:
                        flash("The waste doesn't exist or is sent.", category="danger")
                else:
                    flash("The format is not supported.", category="danger")                             
        return redirect(url_for("scan"))

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        time = datetime.now()
        if form.type.data in ALLOWED_TYPE:
            new = Waste(type=form.type.data, collect_time=time, staff_id=current_user.id)
            db.session.add(new)
            db.session.commit()
            QrGen(new.id, join(app.config["QR_CODE_DIRECTORY"], (str(new.id) + ".jpg")))
            flash(f"Register successfully. Waste ID is {new.id}", category="success")
        else:
            flash("Type is not allowed", category="danger")
    return render_template("register.html", form=form)

@app.route("/library")
@login_required
def library():
    wastes = Waste.query.filter_by(is_sent=False).all()
    return render_template("library.html", wastes=wastes)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = UserSetting()
    if form.validate_on_submit():
        if form.name.data:
            current_user.name = form.name.data
        if form.password.data:
            if form.password.data == form.confirm_password.data:
                current_user.password = bcrypt.generate_password_hash(form.password.data)
            else:
                flash("The two passwords are not same", category="danger")
                return redirect(url_for("admin_staff"))
        if form.phone.data:
            current_user.phone = form.phone.data
        db.session.commit()
    return render_template("settings.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Log out successfully", category="success")
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if app.config["ADMIN_PASSWORD"] == form.password.data:
            flash("Login successfully", category="success")
            if form.page.data == "staff":
                return redirect(url_for("admin_staff"))
            elif form.page.data == "vehicle":
                return redirect(url_for("admin_vehicle"))
    return render_template("admin_login.html", form=form)

@app.route("/admin_staff", methods=["GET", "POST"])
def admin_staff():
    form = AdminStaffForm()
    if form.validate_on_submit():
        if form.id.data:
            staff = Staff.query.filter_by(id=int(form.id.data))
            if staff:
                if form.name.data:
                    staff.name = form.name.data
                if form.password.data:
                    if form.password.data == form.confirm_password.data:
                        staff.password = bcrypt.generate_password_hash(form.password.data)
                    else:
                        flash("The two passwords are not same", category="danger")
                        return redirect(url_for("admin_staff"))
                if form.phone.data:
                    staff.phone = form.phone.data
                db.session.commit()
                flash(f"Staff {form.id}'s information is updated successfully", category="success")
            else:
                flash("The staff doesn't exist", category="danger")
        elif form.name.data and form.phone.data:
            staff = Staff(
                name=form.name.data,
                password=bcrypt.generate_password_hash(form.phone.data),
                phone = form.phone.data
            )
            db.session.add(staff)
            db.session.commit()
            flash(f"New staff {staff.name} has been added", category="success")
        else:
            flash("Required information is missing", category="danger")
    return render_template("admin_staff.html", form=form)

@app.route("/admin_vehicle", methods=["GET", "POST"])
def admin_vehicle():
    form = AdminVehicleField()
    if form.validate_on_submit():
        existed_vehicle = Vehicle.query.filter_by(id=form.id.data)
        if existed_vehicle:
            if form.driver.data:
                existed_vehicle.driver = form.driver.data
            if form.waste_type.data:
                existed_vehicle.waste_type = form.waste_type.data
            db.session.commit()
            flash(f"Vehicle {existed_vehicle.id}'s information is updated.", category="success")
        elif form.id.data and form.driver.data and form.waste_type.data:
            create_vehicle = Vehicle(
                id=form.id.data,
                driver=form.driver.data,
                waste_type=form.waste_type.data
            )
            db.session.add(create_vehicle)
            db.session.commit()
            flash(f"New Vehicle {create_vehicle.id} has been added", category="success")
        else:
            flash("Required information is missing", category="danger")
    return render_template("admin_vehicle.html", form=form)