from flask import Blueprint, request, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor

from flask_login import login_required, current_user
from flask_security import roles_required, roles_accepted

read = Blueprint("read", __name__, template_folder='views')

@read.route("/historico_sensor")
@roles_accepted('Adm', 'Estatico')
def historico_sensor():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template("historico_sensor.html", sensores = sensors, read = read, user = current_user)

@read.route("/get_read", methods=['POST'])
def get_read():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)

        sensors = Sensor.get_sensors()
        return render_template("historico_sensor.html", sensores = sensors, read = read, user = current_user)