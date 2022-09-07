from flask import render_template, flash, redirect, request, url_for, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuarios, Posts
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    posts = Posts.query.order_by(Posts.id.desc())
    return render_template('home.html', posts=posts)

@app.route("/contatos")
def contatos():
    return render_template('contatos.html')

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuarios.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios, enumerate=enumerate)

@app.route("/conta", methods=['GET', 'POST'])
def conta():
    criar_conta = FormCriarConta()
    logar_conta = FormLogarConta()
    if criar_conta.validate_on_submit() and 'botao_criar_conta' in request.form:
        senha_cripy = bcrypt.generate_password_hash(criar_conta.senha.data)
        usuario = Usuarios(email=criar_conta.email.data, usuario=criar_conta.nome_usuario.data, senha=senha_cripy)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o gmail {criar_conta.email.data}', 'alert-success')

        return redirect(url_for('home'))

    if logar_conta.validate_on_submit() and 'botao_logar_conta' in request.form:
        usuario = Usuarios.query.filter_by(email=logar_conta.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, logar_conta.senha.data):
            login_user(usuario, remember=logar_conta.lembra_conta.data)
            flash(f'Login efetuado com sucesso', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Nao foi possivel efetuar o login, verifique se os dados estão corretos ou crie uma conta', 'alert-danger')
    return render_template('conta.html', criar_conta=criar_conta, logar_conta=logar_conta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'logout efetuado com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    foto_perfil = url_for('static', filename='foto perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Posts(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post enviado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

#trata a imagem de perfil do usuario
def imagem_perfil(imagem):
    #mudar nome imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, r'static/foto perfil', nome_arquivo)
    #diminuir tamanho imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    #adicionar imagem banco de dados
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

#filtra os cursos pelo os que o usuario marco

def adicionar_cursos(form):
    lista_auxiliar = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_auxiliar.append(campo.label.text)
    return ';'.join(lista_auxiliar)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.usuario = form.nome_usuario.data
        if form.foto_perfil.data:
            nome_imagem = imagem_perfil(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = adicionar_cursos(form)
        database.session.commit()
        flash(f'Dados atualizados com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.nome_usuario.data = current_user.usuario
    foto_perfil = url_for('static', filename='foto perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Posts.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash(f'Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('exibirPost.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Posts.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash(f'Post excluido com sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route('/perfil/excluir', methods=['GET', 'POST'])
@login_required
def excluir_perfil():
    postsz = Usuarios.query.filter_by(email=current_user.email).first()
    for post in postsz.posts:
        eleminar = Posts.query.get(post.id)
        database.session.delete(eleminar)
        database.session.commit()
    id_pefil = Usuarios.query.get(current_user.id)
    database.session.delete(id_pefil)
    database.session.commit()
    flash(f'Perfil excluido com sucesso', 'alert-success')
    return redirect(url_for('home'))



