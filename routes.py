from flask import render_template, request, redirect, url_for, flash, g

from flask_login import login_user, login_required, logout_user, current_user

from pack import app, db
from pack.models import User, Article, Message


@app.route('/', methods=['GET'])
@login_required
def hello_world():
    return render_template('index.html')


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    article = Article.query.order_by(Article.date).all()
    return render_template('articles.html', article=article)


@app.route('/add_article', methods=['POST', 'GET'])
@login_required
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        db.session.add(Article(title=title, intro=intro, text=text))
        db.session.commit()
        return render_template('articles.html', article=Article.query.all())
    else:
        return render_template('add_article.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and password:
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password2 or password):
            flash('Please fill all fields')
        elif password != password2:
            flash('Passwords are np equal')
        else:
            new_user = User(login=login, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.route("/forum", methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        id_now = current_user.id
        text = request.form['text']
        user = User.query.filter_by(id=id_now).first().login.strip()
        db.session.add(Message(text=text, user_cur=user))
        db.session.commit()
    return render_template("forum.html", message=Message.query.all())


@app.route("/oauth/authorize?response_type=code&client_id=5498456889&redirect_uri=http://127.0.0.1:5000/",
           methods=['GET'])
def auth():
    return render_template("auth.html")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    else:
        return response
