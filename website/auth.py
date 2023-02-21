from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # De __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.Senha, password):
                flash('Login efetuado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='error')
        else:
            flash('Email não cadastrado.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/cadastro_dash', methods=['GET', 'POST'])
def cadastro_dash():
    if request.method == 'POST':
        Permissao = request.form.get('permissao')
        Link = request.form.get('Link')
        Nome = request.form.get('nome')
        Segmento = request.form.get('segmento')

        if len(Link) < 1:
            flash('Insira o link para o dashboard.', category='error')
        elif len(Permissao) < 1:
            flash('insira o nível de permissão.', category='error')
        elif len(Nome) < 1:
            flash('Insira o nome do dashboard.', category='error')
        else:
            novo_cadastro = Note(Permissao=Permissao, Link=Link, Segmento=Segmento,Dashboard=Nome)
            cadastro_all = Note(Permissao="Todas", Link=Link, Segmento=Segmento,Dashboard=Nome)
            db.session.add(novo_cadastro)
            db.session.commit()
            db.session.add(cadastro_all)
            db.session.commit()
            flash('Cadastro concluído!', category='success')
            return redirect(url_for('views.home'))

    return render_template("cadastro_dash.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        permissao = request.form.get('permissao')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('O login já existe.', category='error')
        elif len(email) < 4:
            flash('Login deve ser maior que 3 caracteres.', category='error')
        elif password1 != password2:
            flash('As senhas não correspondem.', category='error')
        elif len(password1) < 7:
            flash('As senhas não correspondem.', category='error')
        else:
            new_user = User(email=email, Permissao=permissao, Senha=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)