from flask import Blueprint, render_template, request, redirect, url_for, flash
from iphone.extensions import db, bcrypt
from iphone.models import User
from flask_login import login_user, logout_user, current_user, login_required

users_bp = Blueprint('users', __name__, template_folder='templates')


# ------------------ USER HOME ------------------
@users_bp.route('/')
@login_required
def index():
  return render_template('users/index.html', title='Dashboard')


# ------------------ REGISTER ------------------
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # 🔥 check username
    if db.session.scalar(db.select(User).where(User.username == username)):
      flash('Username already exists!', 'warning')
      return redirect(url_for('users.register'))

    # 🔥 check email
    if db.session.scalar(db.select(User).where(User.email == email)):
      flash('Email already exists!', 'warning')
      return redirect(url_for('users.register'))

    # 🔥 check password match
    if password != confirm_password:
      flash('Passwords do not match!', 'warning')
      return redirect(url_for('users.register'))

    # 🔥 hash password
    pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    flash('Register successful!', 'success')
    return redirect(url_for('users.login'))

  return render_template('users/register.html', title='Register Page')


# ------------------ LOGIN ------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.session.scalar(db.select(User).where(User.username == username))

    if not user:
      flash('Username not found!', 'warning')
      return redirect(url_for('users.login'))

    if not bcrypt.check_password_hash(user.password, password):
      flash('Incorrect password!', 'warning')
      return redirect(url_for('users.login'))

    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('users.index'))

  return render_template('users/login.html', title='Login Page')


# ------------------ LOGOUT ------------------
@users_bp.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout successful!', 'success')   # ⭐ เพิ่ม
  return redirect(url_for('core.index'))


# ------------------ PROFILE ------------------
@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  user = current_user

  if request.method == 'POST':
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    if firstname and lastname:
      user.firstname = firstname
      user.lastname = lastname
      db.session.commit()

      flash('Profile updated!', 'success')
      return redirect(url_for('users.profile'))

    flash('Please fill all fields!', 'warning')

  return render_template('users/profile.html',
                         title='Profile Page',
                         user=user)


# ------------------ CHANGE PASSWORD ------------------
@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  user = current_user

  if request.method == 'POST':
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')

    # 🔥 check old password
    if not bcrypt.check_password_hash(user.password, old_password):
      flash('Old password incorrect!', 'warning')
      return redirect(url_for('users.change_password'))

    # 🔥 check match
    if new_password != confirm_new_password:
      flash('Passwords do not match!', 'warning')
      return redirect(url_for('users.change_password'))

    # 🔥 update password
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    flash('Password changed successfully!', 'success')
    return redirect(url_for('users.profile'))

  return render_template('users/change_password.html', title='Change Password Page')