from models.db import db
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relacionamento many-to-many com User
    users = db.relationship('User', secondary='userroles', back_populates='roles')

    def add_role(name):
        role = Role.query.filter(Role.name == name).first()

        if role is None:
            role = Role(
                name = name
            )

            db.session.add(role)
            db.session.commit()

    def get_roles():
        roles = Role.query.all()

        return roles