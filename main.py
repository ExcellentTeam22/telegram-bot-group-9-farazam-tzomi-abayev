import json
import random
from flask import Flask, Response, request
import requests
from blood_test_codes import blood_codes

app = Flask(__name__)
TOKEN = '5588135399:AAG55zMzVU4-guuD6MUxtcu3VwP5GSkplYc'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://29a7-2-54-42-153.eu.ngrok.io/message'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
API_URL = "https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&keyword="


def create_keyword_list() -> list:
    """
    Create the list of the keyboard from the user input.
    :return: list of the keywords.
    """
    keywords = get_json(request)["text"].split()
    return keywords[1:]


def create_keyword_search_url() -> str:
    """
    Create the URL for the search of the keywords using this API:
    https://health.gov/our-work/national-health-initiatives/health-literacy/consumer-health-content/free-web-content/apis-developers/api-documentation
    :return: The URL to the API.
    """
    url = API_URL + "".join(create_keyword_list())
    return url


def handle_topic_search() -> list:
    """
    Function to handle the search by keywords.
    :return: The list of articles to show the user.
    """
    response_api = requests.get(url=create_keyword_search_url())
    data = response_api.text
    parse_json = json.loads(data)
    print(parse_json["Result"]["Total"])
    res = list()
    if parse_json["Result"]["Total"] == 0:
        return res
    random_list = random.choices(parse_json["Result"]["Resources"]["Resource"], k=3)
    for i in range(3):
        res.append({"Title": random_list[i]["Title"],
                    "ImageUrl": random_list[i]["ImageUrl"],
                    "ArticleUrl": random_list[i]["AccessibleVersion"]})
    return res


def get_json(req: requests.models.Response) -> dict:
    """
    Function to get the JSON object from the user. in if else format for easier insertion of more message types
    :param req: The request from the user.
    :return: Dictionary of the message data.
    """
    if "edited_message" in request.get_json():
        return req.get_json()["edited_message"]
    else:
        return req.get_json()["message"]


@app.route('/message', methods=["POST"])
def handle_message():
    """
    The main function.
    :return: success response
    """
    ret_img_url = ""
    chat_id = get_json(request)["chat"]["id"]
    first_name = get_json(request)['from']['first_name']
    command = get_json(request)['text'].split()

    if command[0] == "/start":
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, " Welcome {}\n{}".format(first_name, "How can we help?")))

    elif command[0] == "/help":
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "HELP:\n"
                                                   "/tip {key_word} - for receiving recommended articles \n"
                                                   "/blood {KEY} - for deciphering blood tests"))

    elif command[0] == "/tip":
        obj = handle_topic_search()
        ret_value = "For the key: {} Here are some articles that may interest you \n".format(create_keyword_list())
        for article in obj:
            ret_value += article["Title"] + ": \n"
            ret_value += article["ArticleUrl"] + ": \n"
        if obj.__len__() != 0:
            ret_img_url = obj[0]["ImageUrl"]

        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&photo={}"
                           .format(TOKEN, chat_id, "Got message from {}\n{}".format(first_name, ret_value),
                                   ret_img_url))

    elif command[0] == "/blood":
        blood_ret = ""
        for line in blood_codes:
            if line["val0"] == command[1]:
                blood_ret = line["val1"]

        if len(blood_ret) > 0:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                               .format(TOKEN, chat_id, "{}\n{}".format(first_name,
                                                                                        "For the key: {} -> {}".format(command[1],blood_ret))))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                               .format(TOKEN, chat_id, "Sorry {}\n{}".format(first_name,
                                                                                        "There is no such code in the database")))

    else:
        ret_value = "We don't have this command"

        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&photo={}"
                       .format(TOKEN, chat_id, "Got message from {}\n{}".format(first_name, ret_value), ret_img_url))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
