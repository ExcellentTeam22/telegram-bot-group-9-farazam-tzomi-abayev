import json
import random

from flask import Flask, Response, request
import requests
import math

app = Flask(__name__)
TOKEN = '5588135399:AAG55zMzVU4-guuD6MUxtcu3VwP5GSkplYc'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://29a7-2-54-42-153.eu.ngrok.io/message'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
API_URL = "https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&keyword="


@app.route('/')
def home_page():
    return "home page"


def handle_topic_search():
    if "edited_message" in request.get_json():
        keywords = request.get_json()["edited_message"]["text"].split()
    else:
        keywords = request.get_json()["message"]["text"].split()
    keywords = keywords[1:]
    print("keywords", keywords)
    search_string = "%20".join(keywords)
    print("search_string", search_string)
    url = API_URL + "".join(keywords)
    response_api = requests.get(url=url)
    data = response_api.text
    parse_json = json.loads(data)

    random_list = random.choices(parse_json["Result"]["Resources"]["Resource"], k=3)
    res = dict()
    for i in range(3):
        res[i] = {"Title": random_list[i]["Title"],
                  "ImageUrl": random_list[i]["ImageUrl"],
                  "ArticleUrl": random_list[i]["AccessibleVersion"]}
    return res


@app.route('/message', methods=["POST"])
def handle_message():
    print("in got message")
    print(request.get_json())
    print("*" * 20)
    if "edited_message" in request.get_json():
        chat_id = request.get_json()["edited_message"]["chat"]["id"]
        first_name = request.get_json()['edited_message']['from']['first_name']
        command = request.get_json()['edited_message']['text'].split()
    else:
        chat_id = request.get_json()['message']['chat']['id']
        first_name = request.get_json()['message']['from']['first_name']
        command = request.get_json()['message']['text'].split()
    if command[0] == "/tip":
        obj = handle_topic_search()
        print("\nobj = ", obj)
        if "edited_message" in request.get_json():
            keywords = request.get_json()["edited_message"]["text"].split()
        else:
            keywords = request.get_json()["message"]["text"].split()
        keywords = keywords[1:]
        ret_value = "For the key: {} Here are some articles that may interest you \n".format(keywords)
        for article in obj:
            ret_value += obj[article]["Title"] + ": \n"
            ret_value += obj[article]["ArticleUrl"] + ": \n"
        ret_img_url = obj[1]["ImageUrl"]
    else:
        print("in the else")
        ret_value = "We dont have this command"
        ret_img_url = "https://he.m.wikipedia.org/wiki/%D7%A7%D7%95%D7%91%D7%A5:Diagram_of_the_human_heart_%28cropped%29.svg"

    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&photo={}"
                       .format(TOKEN, chat_id, "Got message from {}\n{}".format(first_name, ret_value), ret_img_url))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
