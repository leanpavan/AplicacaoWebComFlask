from flask import Blueprint, request, render_template, redirect, url_for, session
from models.iot.actuators import Actuator
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_security import roles_required, roles_accepted

actuator_ = Blueprint('actuator_', __name__, template_folder='views')

@actuator_.route('/atuadores')
@login_required
def actuators():
    actuators = Actuator.get_actuators()

    return render_template('atuadores.html', atuadores = actuators, user = current_user)

@actuator_.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    Actuator.save_actuator(name, brand, model, topic, unit, is_active)

    actuators = Actuator.get_actuators()

    return render_template("atuadores.html", atuadores = actuators, user = current_user)

@actuator_.route('/edit_actuator')
@roles_required('Adm')
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)

    return render_template("edit_atuador.html", atuador = actuator, user = current_user)

@actuator_.route('/update_actuator', methods=['POST'])
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)

    return render_template("atuadores.html", atuadores = actuators, user = current_user)

@actuator_.route('/del_actuator', methods=['GET'])
def del_actuator():
    id = request.args.get('id', None)
    actuators = Actuator.delete_actuator(id)

    return render_template("atuadores.html", atuadores = actuators, user = current_user)

@actuator_.route('/comandos')
@login_required
@roles_accepted('Adm', 'Operador')
def comandos():
    actuators = Actuator.get_actuators()
    return render_template('comandos.html', user=current_user, atuadores=actuators)