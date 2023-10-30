import flask
from flask import request
import os
from bot import ObjectDetectionBot, Bot
# Botimport sys
# sys.path.append("../../../../py")
# from constants import TELEGRAM_TOKEN, TELEGRAM_APP_URL
# sys.path.append("../PycharmProjects/Docker_Project/docker_yolo_mongo/polybot")
# print(sys.path)
app = flask.Flask(__name__)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']
S3_BUCKET_URL = os.environ.get('S3_BUCKET_URL')


@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL, S3_BUCKET_URL)

    app.run(host='0.0.0.0', port=8443)
    # test
