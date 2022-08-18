from flask import Flask, Response, request
import requests

app = Flask(__name__)
TOKEN = '5529808312:AAG9smQzyXQzGTBt0T0wt-NqUfKW5jpwdko'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                                'https://d0f3-2-54-48-229.eu.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/')
def home_page():
    return "home page"


@app.route('/sanity')
def sanity():
    return "our Server is running good!!!!!!!!!!!!!!!!!! :)) "


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
