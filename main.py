from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session
from datetime import datetime, timedelta
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

users = {
    'ADM': '1234',
    'user1': '1234',
    'user2': '12340'
}
sensors = {}
atuadorDict = {}

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

@app.route('/edit_user')
@login_required
def edit_user():
    user = session['logged_user']
    return render_template('edit_user.html', user = user, users = users)

@app.route('/edit_single_user/<username>')  # Exemplo: /edit_single_user/user1
@login_required
def edit_single_user(username):
    if username in users:
        return render_template('edit_single_user.html', username=username)
    else:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('edit_user'))


@app.route('/delete_user')
@login_required
def delete_user():
    user = session['logged_user']
    return render_template('home.html', user = user)

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
            return redirect(url_for('edit_user'))

        # Atualiza o usuário no dicionário
        if username in users:
            users[newUser] = newPassword  # Adiciona o novo usuário
            if username != newUser:  # Remove o antigo se o nome mudou
                del users[username]
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('edit_user'))

    return redirect(url_for('edit_user'))

@app.route('/new_user')
@login_required
def new_user():
    user = session['logged_user']
    return render_template('new_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users[username] = password

        response = make_response(redirect(url_for('edit_user')))
        return response

@app.route('/registrarSensor')
@login_required
def registrarSensor():
    user = session['logged_user']
    return render_template('registrarSensor.html', user=user)

@app.route('/ADDsensor', methods=['POST'])
@login_required
def ADDsensor():
    user = session['logged_user']
    global sensors
    if request.method == 'POST':
        InputSensor = request.form['sensor']
        sensors[InputSensor] = "-1"

        return render_template('sensores.html',user=user, sensors=sensors)

@app.route('/registrarAtuador')
@login_required
def registrarAtuador():
    user = session['logged_user']
    return render_template('registrarAtuador.html', user=user)

@app.route('/ADDatuador', methods=['POST'])
@login_required
def ADDatuador():
    user = session['logged_user']
    global atuadorDict
    if request.method == 'POST':
        InputAtuador = request.form['atuador']
        atuadorDict[InputAtuador] = "-1"

        return render_template('atuadores.html', user=user, atuadores=atuadorDict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8084, debug=True)