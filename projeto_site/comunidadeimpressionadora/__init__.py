from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '98382dfc4e4a868ff242c152f0ddb44e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maneger = LoginManager(app)
login_maneger.login_view = 'conta'
login_maneger.login_message = 'Para acessar esta pagina efetue login ou crie uma conta'
login_maneger.login_message_category = 'alert-info'


from comunidadeimpressionadora import route