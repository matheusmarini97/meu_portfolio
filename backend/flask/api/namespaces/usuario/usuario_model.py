from api import db

class UsuarioModel(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(200), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    data_nascimento = db.Column(db.DateTime, nullable = False)