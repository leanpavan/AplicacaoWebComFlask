from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, jsonify
from datetime import datetime, timedelta
import secrets
from functools import wraps

from flask_mqtt import Mqtt
from flask_socketio import SocketIO

import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

mqtt_client= Mqtt()
mqtt_client.init_app(app)

topic_subscribe = "projeto_cavalo" # Topico do projeto

users = {
    'ADM': '1234',
    'user1': '1234',
    'user2': '12340'
}
sensors = {
    "Temperatura": -1,
    "Ultrassonico": -1
}
atuadorDict = {
    "LED_Vermelho": 0,
    "LED_Amarelo": 0,
    "LED_Azul": 0,
    "Servo_Motor": 0
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    username = request.cookies.get('remembered_user')
    return render_template('login.html', remembered_user = username)

@app.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        print(user, password)
        if user in users and users[user] == password:

            session['logged_user'] = user

            response = make_response(redirect(url_for('home')))

            if remember_me:
                expires = datetime.now() + timedelta(days=30)
                response.set_cookie('remembered_user', user, expires=expires)

            return response
        else:
            flash('Credenciais inválidas! Tente novamente.', 'error')
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    user = session['logged_user']
    return render_template('home.html', user = user)

@app.route('/sobre')
@login_required
def sobre():
    user = session['logged_user']
    return render_template('sobre.html', user = user)

@app.route('/sensores')
@login_required
def sensores():
    global sensors
    user = session['logged_user']
    return render_template('sensores.html', user=user, sensors=sensors)

@app.route('/atuadores')
@login_required
def atuadores():
    global atuadorDict
    user = session['logged_user']
    return render_template('atuadores.html', user=user, atuadores=atuadorDict)

@app.route('/tempo_real')
@login_required
def tempo_real():
    user = session['logged_user']

    global sensors

    return render_template('tempo_real.html', user=user, sensores=sensors)

@app.route('/comandos')
@login_required
def comandos():
    user = session['logged_user']
    
    global atuadorDict
    return render_template('comandos.html', user=user, atuadores=atuadorDict)

@app.route('/user')
@login_required
def user():
    user = session['logged_user']
    return render_template('user.html', user = user, users = users)

@app.route('/edit_single_user/<username>')  # Exemplo: /edit_single_user/user1
@login_required
def edit_single_user(username):
    user = session['logged_user']
    if username in users:
        return render_template('edit_single_user.html', username=username, user=user)
    else:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('user'))

@app.route('/delete_user/<username>')
@login_required
def delete_user(username):
    global users

    user = session['logged_user']

    if username in users:
        users.pop(username)
    else:
        flash('Usuario não encontrado!', 'error')

    return render_template('user.html', user = user, users=users)

@app.route('/update_user', methods=['POST'])  # Adicione methods=['POST']
@login_required
def update_user():
    if request.method == 'POST':
        newUser = request.form['newUsername']
        newPassword = request.form['newPassword']
        username = request.form['currentUser']  # Certifique-se de que esse campo está sendo enviado (troque disabled por readonly)

        # Verifica se o novo nome já existe
        if newUser in users:
            flash('Usuário já existe! Escolha outro nome.', 'error')
            return redirect(url_for('user'))

        # Atualiza o usuário no dicionário
        if username in users:
            users[newUser] = newPassword  # Adiciona o novo usuário
            if username != newUser:  # Remove o antigo se o nome mudou
                del users[username]
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('user'))
        else:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('user'))

    return redirect(url_for('user'))

@app.route('/add_user', methods=['POST'])
def add_user():
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users[username] = password

        response = make_response(redirect(url_for('user')))
        return response

@app.route('/ADDsensor', methods=['POST'])
@login_required
def ADDsensor():
    user = session['logged_user']
    global sensors
    if request.method == 'POST':
        InputSensor = request.form['sensor']
        sensors[InputSensor] = "-1"

        return render_template('sensores.html',user=user, sensors=sensors)
    
@app.route('/delete_sensor/<sensor>')
@login_required
def delete_sensor(sensor):
    global sensors

    user = session['logged_user']

    if sensor in sensors:
        sensors.pop(sensor)
    else:
        flash('Sensor não encontrado!', 'error')

    return render_template('sensores.html', user = user, sensors=sensors)

@app.route('/edit_sensor/<sensor>')
@login_required
def edit_sensor(sensor):
    user = session['logged_user']
    if sensor in sensors:
        return render_template('edit_sensor.html', sensor=sensor, user=user)
    else:
        flash('Sensor não encontrado!', 'error')
        return redirect(url_for('sensores'))

@app.route('/update_sensor', methods=['POST'])
@login_required
def update_sensor():
    if request.method == 'POST':
        newSensor = request.form['newSensor']
        sensor = request.form['currentSensor']

        # Verifica se o novo nome já existe
        if newSensor in sensors:
            flash('Sensor já existe! Escolha outro nome.', 'error')
            return redirect(url_for('sensores'))

        # Atualiza o sensor no dicionário
        if sensor in sensors:
            sensors[newSensor] = -1  # Adiciona o novo sensor
            if sensor != newSensor:  # Remove o antigo se o nome mudou
                del sensors[sensor]
            flash('Sensor atualizado com sucesso!', 'success')
            return redirect(url_for('sensores'))
        else:
            flash('Sensor não encontrado!', 'error')
            return redirect(url_for('sensores'))

    return redirect(url_for('sensores'))


@app.route('/ADDatuador', methods=['POST'])
@login_required
def ADDatuador():
    user = session['logged_user']
    global atuadorDict
    if request.method == 'POST':
        InputAtuador = request.form['atuador']
        atuadorDict[InputAtuador] = 0

        return render_template('atuadores.html', user=user, atuadores=atuadorDict)

@app.route('/delete_atuador/<atuador>')
@login_required
def delete_atuador(atuador):
    global atuadorDict

    user = session['logged_user']

    if atuador in atuadorDict:
        atuadorDict.pop(atuador)
    else:
        flash('Atuador não encontrado!', 'error')

    return render_template('atuadores.html', user = user, atuadores=atuadorDict)

@app.route('/edit_atuador/<atuador>')
@login_required
def edit_atuador(atuador):
    user = session['logged_user']
    if atuador in atuadorDict:
        return render_template('edit_atuador.html', atuador=atuador, user=user)
    else:
        flash('Atuador não encontrado!', 'error')
        return redirect(url_for('atuadores'))

@app.route('/update_atuador', methods=['POST'])
@login_required
def update_atuador():
    if request.method == 'POST':
        newAtuador = request.form['newAtuador']
        atuador = request.form['currentAtuador']

        # Verifica se o novo nome já existe
        if newAtuador in atuadorDict:
            flash('Sensor já existe! Escolha outro nome.', 'error')
            return redirect(url_for('sensores'))

        # Atualiza o sensor no dicionário
        if atuador in atuadorDict:
            atuadorDict[newAtuador] = -1  # Adiciona o novo sensor
            if atuador != newAtuador:  # Remove o antigo se o nome mudou
                del atuadorDict[atuador]
            flash('Atuador atualizado com sucesso!', 'success')
            return redirect(url_for('atuadores'))
        else:
            flash('Atuador não encontrado!', 'error')
            return redirect(url_for('atuadores'))

    return redirect(url_for('atuadores'))

@app.route('/publish_message', methods=['GET','POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)

# Conexões mqtt
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe) # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global sensors
    print(message.payload.decode())
    js = json.loads(message.payload.decode())
    if(js["sensor"]=="projeto_cavalo/temperatura"):
        sensors['Temperatura'] = js["valor"]
    elif(js["sensor"]=="projeto_cavalo/ultrassonico"):
        sensors['Ultrassonico'] = js["valor"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8084, debug=True)