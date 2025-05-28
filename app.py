# app.py
from controllers.app_controller import create_app
from flask import Flask, render_template, request
from utils.create_db import create_db

app= Flask(__name__)

if __name__ == "__main__":
    app = create_app()
    create_db(app)
    app.run(host='0.0.0.0', port=8084, debug=True)