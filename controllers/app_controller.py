from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash, jsonify
from models.db import db, instance
from models.user.user import User
from models.user.role import Role

from datetime import datetime, timedelta
import secrets

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_security import Security, SQLAlchemyUserDatastore, roles_required, roles_accepted

from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from controllers.sensors_controller import sensor_
from controllers.user_controller import user_
from controllers.actuators_controller import actuator_

import json

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe = "projeto_cavalo" # Topico do projeto

    app.register_blueprint(sensor_, url_prefix='/') # Registra Blueprint dos sensors
    app.register_blueprint(user_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')

    db.init_app(app)


    # Inicialização do LoginManager do flask_login, para autenticação de usuario
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_id(user_id)
    
    #Inicialização do flask_security, para autenticação de roles
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @app.route('/')
    def index():
        username = request.cookies.get('remembered_user')
        return render_template('login.html', remembered_user=username)

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html', user=current_user)

    @app.route('/sobre')
    @login_required
    def sobre():
        return render_template('sobre.html', user = current_user)

    @app.route('/tempo_real')
    @login_required
    @roles_accepted('Adm', 'Estatico')
    def tempo_real():
        global sensors

        return render_template('tempo_real.html', user=current_user, sensores=sensors)

    @app.route('/comandos')
    @login_required
    @roles_accepted('Adm', 'Operador')
    def comandos():
        global atuadorDict
        return render_template('comandos.html', user=current_user, atuadores=atuadorDict)

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


    return app