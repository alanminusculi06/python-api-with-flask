from sql_alchemy import db
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    login = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, id, name, login, password):
        self.id = id
        self.name = name
        self.login = login
        self.password = generate_password_hash(password) 
        
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "login": self.login
        }
        
    @classmethod
    def find_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()