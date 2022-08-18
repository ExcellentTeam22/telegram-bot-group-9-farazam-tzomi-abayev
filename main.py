from flask import Flask, Response, request
import requests
import math

app = Flask(__name__)
TOKEN = '5529808312:AAG9smQzyXQzGTBt0T0wt-NqUfKW5jpwdko'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://d0f3-2-54-48-229.eu.ngrok.io/message'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


def is_prime(number: str) -> str:
    number = int(number)
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return "the {} is not prime".format(number)
        return "{} is prime".format(number)


def factorial(number: str) -> str:
    number = int(number)
    fact = 1

    for i in range(1, number + 1):
        fact = fact * i
    return "the factorial of the {} is {}".format(number, fact)


def is_palindrome(word: str) -> str:
    palindrome = word == word[::-1]
    return "{} is {} palindrome".format(word, " " if palindrome else "not")


def sqrt(number: str) -> str:
    number = int(number)
    root = math.sqrt(number)
    # return int(root + 0.5) ** 2 == number
    has_sqrt = int(root + 0.5) ** 2 == number
    return "{} {} an integer square root".format(number, "have" if has_sqrt else "not have")


route_dictionary = {"/prime": is_prime,
                    "/factorial": factorial,
                    "/palindrome": is_palindrome,
                    "/sqrt": sqrt}


@app.route('/')
def home_page():
    return "home page"


@app.route('/message', methods=["POST"])
def handle_message():
    print("in got message")
    chat_id = request.get_json()['message']['chat']['id']
    first_name = request.get_json()['message']['from']['first_name']
    command = request.get_json()['message']['text'].split()
    print(command)
    if command[0] in route_dictionary:
        print("in the if")
        ret_value = route_dictionary[command[0]](str(command[1]))
    else:
        print("in the else")
        ret_value = "We dont have this command"
    print("*"*20)
    print(ret_value)
    print("*"*20)
    print(request.get_json()['message']['text'])
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "Got message from {}\n{}".format(first_name, ret_value)))
    return Response("success")


@app.route('/prime', methods=["POST"])
def is_prime():
    print("in is prime function")
    chat_id = request.get_json()['message']['chat']['id']
    print(request.get_json())
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
