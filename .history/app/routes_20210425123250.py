import threaded
from flask import render_template, request, redirect, make_response
from app import app, sql
import secrets
import telebot

app.secret_key = 'any random string';
bot = telebot.TeleBot("1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.reply_to(message, "This is a message handler")

@app.route('/api/login', methods=["POST"])
def api_login():
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])

            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/api/signup', methods=["POST"])
def api_signup():
    sql.Person(login=request.form['login'], password=request.form['password']).save()
    return redirect("/", code=302)

@app.route('/api/telegram/sendMessage/<chat_id>/<text>', methods=["GET"])
def sendMessage(chat_id, text):
    return {"sent": True, "chat_id": chat_id} if bot.send_message(chat_id, text) else {"sent": False, "chat_id": chat_id}

@app.route('/api/telegram/getUpdates/<chat_id>', methods=["GET"])
def getUpdates(chat_id):
    print(bot.get_updates())
    return bot.get_updates()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@app.route('/login')
def route_login():
    return render_template('login.html', title='Вход в систему')

@app.route('/signup')
def route_signup():
    return render_template('signup.html', title='Регистрация в системе')

@app.route('/')
def route_dashboard():
    if 'login' in request.cookies:
        return render_template('dashboard.html', title='Рабочая область', login=request.cookies['login'])
    else:
        return redirect("/login", code=302)

@threaded.ThreadPooled
def func():
    bot.polling()