from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import telebot

if __name__ == "__main__":

    app = Flask(__name__, 
        static_url_path='', 
        static_folder='static',
        template_folder='templates'
    )

    sockets = Sockets(app)

    @sockets.route('/echo')
    def echo_socket(ws):
        while not ws.closed:
            message = ws.receive()
            ws.send(message)

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

    bot = telebot.TeleBot("1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

    from app import routes
    from app import flow