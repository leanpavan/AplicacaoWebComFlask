from flask import Flask, render_template, request

app = Flask(__name__)

users = {
    "ADM": "1234",
    "user1": "123"
    }

usuario_logado = ""

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        usuario_logado = user

        if user in users and users[user] == password:
            return render_template('home.html', user=usuario_logado)
        else:
            return '<h1>Credenciais invalidas</h1>'
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sensores.html')
def sensores():
    return render_template('sensores.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)