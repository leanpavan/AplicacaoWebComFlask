from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

users = {
    'user1': '1234',
    'user2': '12340'
}

@app.route('/')
def index():
    username = request.cookies.get('remembered_user')
    return render_template('login.html', remembered_user = username)

@app.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        print(user, password)
        if user in users and users[user] == password:
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
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8084, debug=True)