from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Medication(db.Model):
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    medName = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255), nullable=True)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
