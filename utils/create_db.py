from flask import Flask
from models import *
from utils.inicializar_dado import Inicializar

def create_db(app:Flask):
    with app.app_context():
        db.create_all()
        if Inicializar.create_roles_user():
            print('usuarios e roles cadastrados')
        else:
            print("nada inserido")