import threaded
import service
from app import app, bot, socketio
from flask_cors import CORS
    
CORS(app)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':

    @threaded.ThreadPooled
    def polling():
        bot.polling()

    polling()

    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()

    socketio.run(app, port=5003)
