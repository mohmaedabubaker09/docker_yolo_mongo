import flask
from flask import request
import os
import time
import datetime
from bot import ObjectDetectionBot, Bot, QuoteBot
# Botimport sys
# sys.path.append("../../../../py")
# from constants import TELEGRAM_TOKEN, TELEGRAM_APP_URL
# sys.path.append("../PycharmProjects/Docker_Project/docker_yolo_mongo/polybot")
# print(sys.path)
app = flask.Flask(__name__)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']
S3_BUCKET_URL = os.environ.get('S3_BUCKET_URL')
"""
s3_access_key = os.environ['S3_ACCESS_KEY']
s3_secret_key = os.environ['S3_SECRET_KEY']
"""

@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":

    # bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL, S3_BUCKET_URL)
    bot = Bot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)
    #bot = QuoteBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    # print("Flask Server Begin:", datetime.now().strftime('%H:%M:%S'))
    app.run(host='0.0.0.0', port=8443)
    # test
