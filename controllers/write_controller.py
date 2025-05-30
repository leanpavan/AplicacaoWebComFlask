from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator

from flask_login import login_required, current_user
from flask_security import roles_required, roles_accepted

write = Blueprint("write", __name__, template_folder='views')

@write.route("/historico_atuador")
@roles_accepted('Adm', 'Operador')
def historico_atuador():
    actuators = Actuator.get_actuators()
    write = {}
    return render_template("historico_atuador.html", actuators = actuators, write = write, user = current_user)

@write.route("/get_write", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)

        actuators = Actuator.get_actuators()
        return render_template("historico_atuador.html", actuators = actuators, write = write, user = current_user)