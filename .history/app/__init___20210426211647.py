from flask import Flask
from flask_socketio import SocketIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import telebot

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

bot = telebot.TeleBot(
    "1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

from app import routes
from app import flow