from flask import Blueprint, request, render_template, redirect, url_for, session, flash, make_response
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_security import roles_required

from models.user.user import User
from models.user.role import Role

from werkzeug.security import generate_password_hash, check_password_hash

user_ = Blueprint('user_', __name__, template_folder='views')
    
@user_.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember_me') else False

    user = User.get_user_login(email)

    if not user or not check_password_hash(user.password, password):
        flash('Credenciais inválidas, tente novamente!')
        return redirect(url_for('index'))
    
    login_user(user, remember=remember)
    return redirect(url_for('home'))

@user_.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@user_.route('/user')
@login_required
@roles_required('Adm')
def user():
    users = User.get_users()
    roles = Role.get_roles()

    return render_template('user.html', user = current_user, users = users, roles = roles)

@user_.route('/add_user', methods=['POST'])
def add_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('role_type_')

    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Ve se o usuario já existe
    user = User.get_user_login(email)
    if user:
        flash("E-mail já cadastrado!")
    else:
        User.add_user(name, email, password_hash, role)
    
    users = User.get_users()
    roles = Role.get_roles()

    return render_template('user.html', users = users, roles = roles, user = current_user)

@user_.route('/edit_user')
@login_required
@roles_required('Adm')
def edit_user():
    id = request.args.get('id', None)
    user_edit = User.get_single_user(id)
    roles = Role.get_roles()

    return render_template('edit_user.html', username = user_edit, roles = roles, user = current_user)

@user_.route('/update_user', methods=['POST'])
def update_user():
    id = request.form.get("id")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    is_active = True if request.form.get("is_active") == "on" else False
    role = request.form.get("role_type_")

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    users = User.update_user(id, name, email, password_hash, is_active, role)
    roles = Role.get_roles()

    return render_template('user.html', user = current_user, users = users, roles = roles)

@user_.route('/del_user')
@login_required
@roles_required('Adm')
def del_user():
    id = request.args.get('id', None)
    users = User.delete_user(id)
    roles = Role.get_roles()

    return render_template('user.html', user = current_user, users = users, roles = roles)