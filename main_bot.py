'''
Telegram Rmovie Bot that use API from site sashamoran.pythonanywhere.com.
'''
import re

from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests

from config import TOKEN


URL = f'https://api.telegram.org/bot{TOKEN}/'
commands = ['/start', '/rmovie']

app = Flask(__name__)
sslify = SSLify(app)


def send_messages(chat_id, text='Please wait', parse_mode='HTML'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    r = requests.post(url, json=answer)
    return r.json()


def get_randmovie():
    URL = 'http://sashamoran.pythonanywhere.com/api/randmovie/'
    r = requests.get(URL)
    response = r.json()
    movie = '<b>Название:</b> ' + response['title'] + \
            '\n' + '<b>О фильме:</b> ' +  response['text'] + \
            '\n' + '<b>Трейлер:</b> ' +  response['link']
    return movie


def get_respond_cmd(text):
    pattern = r'/\w+'
    if re.search(pattern, text):
        return text
    else:
        return None


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        print(r)
        chat_id = r['message']['chat']['id']
        command = r['message']['text']
        cmd = get_respond_cmd(command)
        if get_respond_cmd(command) == None:
            send_messages(chat_id, 'Не понял Вас(')
        else:
            if cmd == '/start':
                send_messages(chat_id, '🛠<b>Список команд:</b>\n▪️/rmovie - получить случайный фильм.')
            elif cmd == '/rmovie':
                send_messages(chat_id,  get_randmovie())
            elif cmd not in commands:
                send_messages(chat_id, 'Данная команда не найдена!')
        return jsonify(r)
    return "<h1>Welcome to bot's page!</h1>"

if __name__ == '__main__':
    app.run()
