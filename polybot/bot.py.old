import telebot
from loguru import logger
import os
import time
import datetime
from telebot.types import InputFile
import requests
import boto3

class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):

        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        # print("Sending message to Telegram at time:", datetime.now().strftime('%H:%M:%S'))
        self.send_text(msg['chat']['id'], f'Your original message from Mohammad: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ObjectDetectionBot(Bot):

    def __init__(self, token, telegram_chat_url, S3_BUCKET_URL):
        # s3_access_key , s3_secret_key
        super().__init__(token, telegram_chat_url)
        self.S3_BUCKET_URL = S3_BUCKET_URL
        """
        self.S3_ACCESS_KEY = s3_access_key
        self.S3_SECRET_KEY = s3_secret_key
        self.s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
        """
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if self.is_current_msg_photo(msg):
            try:
                # Download the user photo
                img_path = self.download_user_photo(msg)

                # Upload the photo to S3
                s3_url = self.upload_to_s3(img_path)

                # Send a request to the `yolo5` service for prediction
                yolo_prediction = self.request_yolo_prediction(s3_url)

                # Send results to the Telegram end-user
                self.send_text(msg['chat']['id'], f'YOLO Prediction: {yolo_prediction}')

            except Exception as e:
                logger.error(f'Error processing message: {e}')

    def upload_to_s3(self, img_path):
        # Assuming you have AWS credentials configured in the environment or using a secure method
        # Upload logic here, using boto3 or a suitable library
        """
        try:
            # to be updated
            self.s3_client.upload_file(str(predicted_img_path), images_bucket, s3_prediction_img_path)
        except Exception as e:
            logger.error(e)
            raise
            return
        """
    def request_yolo_prediction(self, s3_url):
        # Assuming you have an endpoint where YOLO5 service is running
        yolo_endpoint = 'http://yolo5-service-endpoint/predict'
        response = requests.post(yolo_endpoint, params={'imgName': s3_url})

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


            # TODO download the user photo (utilize download_user_photo)
            # TODO upload the photo to S3
            # TODO send a request to the `yolo5` service for prediction
            # TODO send results to the Telegram end-user
