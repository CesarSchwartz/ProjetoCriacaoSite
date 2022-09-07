from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuarios
from flask_login import current_user


#criando classes formularios

class FormCriarConta(FlaskForm):
    nome_usuario = StringField('Nome Usuario', validators=[DataRequired(message='Digite um nome de usuario')])
    email = StringField('Gmail', validators=[DataRequired(), Email(message='Digite um email valido')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirma_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha', message='A senha deve ser igual ao campo senha')])
    botao_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email existente. cadastra-se com outro email ou faça login')


class FormLogarConta(FlaskForm):
    email = StringField('Gmail', validators=[DataRequired(), Email(message='Digite um email valido')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_logar_conta = SubmitField('Logar')
    lembra_conta = BooleanField('lembrar dados de acesso')

class FormEditarPerfil(FlaskForm):
    nome_usuario = StringField('Nome Usuario', validators=[DataRequired(message='Digite um nome de usuario')])
    email = StringField('email', validators=[DataRequired(), Email(message='Digite um email valido')])
    foto_perfil = FileField('atualizar foto perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField('Excel impressionador')
    curso_python = BooleanField('Python impressionador')
    curso_vba = BooleanField('VBA impressionador')
    curso_sql = BooleanField('SQL impressionador')
    curso_power = BooleanField('Power BI impressionador')
    curso_apresentaçoes = BooleanField('Apresentações impressionador')
    botao_editar_perfil = SubmitField('Comfirmar ediçao')


    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuarios.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email existente. coloque outro email')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(5, 140)])
    corpo = TextAreaField('Corpo do Post', validators=[DataRequired()])
    botao_criar_post = SubmitField('Enviar Post')
