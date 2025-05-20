from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        db.create_all()