from flask import Blueprint, render_template, url_for, redirect, flash, session
from flask_login import login_required, current_user
from pythonic import db, bcrypt
from pythonic.users.forms import RegistrationForm, VerifyForm, LoginForm 
from pythonic.models import User, Device, Request, VerificationCode
from pythonic import mail
from flask_mail import Message
import random

users = Blueprint('users', __name__)

def generate_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    msg = Message(
        subject="Stor Verification Code",
        sender="plarosite@gmail.com",
        recipients=[email]
    )
    msg.body = f"Your verification code for Stor is: {code}"
    mail.send(msg)



@users.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():

        existing = VerificationCode.query.filter_by(form.eamil.data)
        if existing:
            db.session.delete(existing)
            db.session.commit()

        code = generate_code
        record = VerificationCode(email=form.email.data)
        db.session.add(record)
        db.session.commit()

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('users.register'))


        session['user_register_data'] = {
            'username': form.username.data,
            'email': form.email.data,
            'password': hashed_password
        }

        send_verification_email(form.email.data, code)
        flash('A verification code has been sent to your email.', 'info')
        return redirect(url_for('users.verify'))
    return render_template('register.html', form=form)





@users.route('/verify', methods=["GET", "POST"])
def verify():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = VerifyForm()
    data = session.get("user_register_data")
    if not data:
        flash(f"Registeration expired. Please register again", "Warning")
        return redirect(url_for('users.register'))
    
    if form.validate_on_submit():
        email = data['email']
        recorde = VerificationCode.query.filter_by(email=email).first()
        if not recorde:
            flash(f"No verifcation code found", "danger")
            session.pop('user_register_data', None)
            return redirect(url_for('users.register'))
        
        if recorde.is_expired():
            db.session.delete(recorde)
            db.session.commit()
            flash(f"verifcation code expired", "danger")
            session.pop('user_register_data', None)
            return redirect(url_for('users.register'))
        
        if form.code.data != recorde.code:
            flash("Incorrect verifcation code", "danger")
            return redirect(url_for('users.verify'))
        
        hashed_password = data['password']
        user = User(name=data['name'], email=data['email'], password=hashed_password)

        db.session.add(user)
        db.session.commit()

        db.session.delete(recorde)
        db.session.commit()

        session.pop('user_register_data', None)
        flash(f"Account createed successfully. you can now log in", "seccess")
        return redirect(url_for('users.login'))
    return render_template('verify.html')



@users.route('/resend_code', methods=["GET", "POST"])
def resend_code():
    data = session.get['user_register_data']
    if not data:
        flash(f"Registeration expired", "warning")
        return redirect(url_for('users.register'))
    
    email = data['email']
    record = VerificationCode.query.filter_by(email=email.data)
    if record():
        db.session.delete(record)
        db.session.commit()

    code = generate_code()
    new_record = VerificationCode(email=email.data, code)
    return redirect(url_for('user.verify'))


@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        return redirect(url_for('main.home'))
    return render_template('login.html')






@users.route('/device/<int:device_id>/buy')
@login_required
def buy_device(device_id):
    device = Device.query.get_or_404(device_id)

    request = Request(user_id=current_user.id, device_id=device.id)
    db.session.add(request)
    db.session.commit()

    flash("Your request has been submitted successfully.", "success")
    return redirect(url_for('main.home'))

