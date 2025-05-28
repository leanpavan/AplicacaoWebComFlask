from flask import Blueprint, request, render_template, redirect, url_for, session
from models.iot.sensors import Sensor
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_security import roles_required, roles_accepted

sensor_ = Blueprint("sensor_", __name__, template_folder="templates")

@sensor_.route('/sensores')
@login_required
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensores.html", sensors = sensors, user = current_user)

@sensor_.route('/register_sensor')
def register_sensor():
    return render_template("registrarSensor.html")

@sensor_.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(name, brand, model, topic, unit, is_active)

    sensors = Sensor.get_sensors()
    return render_template("sensores.html", sensors = sensors, user = current_user)

@sensor_.route('/edit_sensor')
@roles_accepted('Adm')
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("edit_sensor.html", sensor = sensor, user = current_user)


@sensor_.route('/update_sensor', methods=['POST'])
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    return render_template("sensores.html", sensors = sensors, user = current_user)

@sensor_.route('/del_sensor', methods=['GET'])
def del_sensor():
    id = request.args.get('id', None)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensores.html", sensors = sensors, user = current_user)