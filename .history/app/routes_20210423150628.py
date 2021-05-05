from flask import render_template, request, redirect, make_response
from app import app, sql

app.secret_key = 'any random string';

@app.route('/api/login', methods=["POST"])
def login():
    # sql.Person(login=request.form['login'], password=request.form['password']).save()
    
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])

            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/login')
def index():
    return render_template('index.html', title='Домашний экран')

@app.route('/')
def dashboard():
    if 'login' in request.cookies:
        return render_template('dashboard.html', title='Рабочая область')
    else:
        redirect("/login", code=302)
    