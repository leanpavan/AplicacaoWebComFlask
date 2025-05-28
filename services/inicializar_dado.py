from models.user.user import User
from models.user.role import Role
from werkzeug.security import generate_password_hash

class Inicializar:
    def create_roles_user():
        if not Role.query.first():
            Role.add_role('Adm')
            Role.add_role('Estatico')
            Role.add_role('Operador')

        if not User.query.first():
            senha = '1234'
            senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
            User.add_user('ADM', 'adm@adm.com', senha_hash, 'Adm')
            User.add_user('User1', 'user1@gmail.com', senha_hash, 'Estatico')
            User.add_user('User2', 'user2@gmail.com', senha_hash, 'Operador')