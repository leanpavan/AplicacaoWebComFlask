from models.db import db
from models.user.role import Role
from models.user.user import User

class UserRoles(db.Model):
        __tablename__ = 'userroles'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
        role_id = db.Column(db.Integer, db.ForeignKey(Role.id, ondelete='CASCADE'))