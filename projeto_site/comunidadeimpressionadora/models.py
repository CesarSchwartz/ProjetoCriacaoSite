from comunidadeimpressionadora import database, login_maneger
from datetime import datetime
from flask_login import UserMixin

@login_maneger.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario))

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.png')
    posts = database.relationship('Posts', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='nao informado')

    def contar_post(self):
        return len(self.posts)


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)
