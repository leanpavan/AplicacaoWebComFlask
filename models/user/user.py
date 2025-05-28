from models.db import db
from flask_login import UserMixin
from flask_security import UserMixin
from models.user.role import Role

import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    active = db.Column(db.Boolean())

    # Campo fd_uniquifier
    fs_uniquifier = db.Column(db.String(255), unique=True, default=lambda:str(uuid.uuid4()))

    # Relacionamento many-to-many com Role
    roles = db.relationship('Role', secondary='userroles', back_populates='users')


    def add_user(name, email, password, role):
        user = User.query.filter(User.email == email).first()

        if user is None:
            user = User(
                name = name,
                email = email,
                password = password,
                active = True
            )

            role_user = Role.query.filter(Role.name == role).first()
            if role_user is not None:
                user.roles.append(role_user)

            db.session.add(user)
            db.session.commit()

    def get_user_id(id):
        return User.query.get(int(id))
    
    def get_user_login(email):
        user = User.query.filter(User.email == email).first()
        return user
    
    def has_role(self, role_name):
        """Verifica se o usuário tem uma role específica."""
        return any(role.name == role_name for role in self.roles)
    
    def get_users():
        users = User.query.all()

        return users
    
    def get_single_user(id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            return [user]

        return None
    
    def update_user(id, name, email, password, is_active, role):
        user = User.query.filter(User.id == id).first()

        if user is not None:
            user.name = name
            user.email = email
            user.password = password
            user.active = is_active

            if role:
                role_user = Role.query.filter(Role.name == role).first()
                if role_user:
                    user.roles = [role_user]

            db.session.commit()

            return User.get_users()
        return None
    
    def delete_user(id):
        user = User.query.filter(User.id == id).first()

        db.session.delete(user)
        db.session.commit()

        return User.get_users()