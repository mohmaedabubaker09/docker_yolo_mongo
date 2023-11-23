import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import boto3
import requests
import json
import botocore
from openai import OpenAI
from io import BytesIO
from PIL import Image

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

        # logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')


    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    # def send_text_with_quote(self, chat_id, text, quoted_msg_id):
    #     self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

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
        # folder_name = ""

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
        # logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


# class QuoteBot(Bot):
#     def handle_message(self, msg):
#         logger.info(f'Incoming message: {msg}')
#
#         if msg["text"] == 'How are you':
#             self.send_text(msg['chat']['id'], "Fine Thank You!")
#         elif msg["text"] != 'Please don\'t quote me':
#             self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])

class ObjectDetectionBot(Bot):

    # TODO download the user photo (utilize download_user_photo) - Done!
    # TODO upload the photo to S3 - Done!
    # TODO send a request to the `yolo5` service for prediction - Done!
    # TODO send results to the Telegram end-user - Done!

    def __init__(self, token, telegram_chat_url):
        Bot.__init__(self, token, telegram_chat_url)
        self.chat_gpt_client = OpenAI()
        # self.chat_gpt_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'],)

        self.Bucket_Name = os.environ['BUCKET_NAME']
        self.aws_region = os.environ['REGION']
        # self.s3_client = boto3.client('s3', aws_access_key_id=self.s3_access_key, aws_secret_access_key=self.s3_secret_key)
        self.s3_resource = boto3.resource(
           's3',
            region_name=self.aws_region,
            aws_access_key_id=os.environ['S3_ACCESS_KEY'],
            aws_secret_access_key=os.environ['S3_SECRET_KEY']
        )

    def dalle_generate_image(self, prompt):
        try:
            response = self.chat_gpt_client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt}",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            print(f"An error occurred while generating image in DALL-E: {e}")

    def save_dalle_image(self, image_url, file_path):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image.save(file_path)
            print(f"Image saved to {file_path}")
        except Exception as e:
            print(f"Failed to save image: {e}")

    def handle_message(self, msg):
        # self.send_text(msg['chat']['id'], "Hello, talk to me habibi")
        if not (self.is_current_msg_photo(msg)):
            completion = self.chat_gpt_client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system",
                     "content": "You are a precise, swift, funny, friendly, and to the point assistant. You use emojies. Your name is LanaScoop."},
                    {"role": "user", "content": msg["text"] }
                ]
            )
            # Extract just the content of the message
            response_content = completion.choices[0].message.content if completion.choices[0].message else None

            if response_content:
                # Format the content for readability
                formatted_response = response_content.strip()
                self.send_text(msg['chat']['id'], formatted_response)
            else:
                # Handle cases where the content is None or empty
                error_message = "Sorry, I couldn't generate a response. Please try again."
                self.send_text(msg['chat']['id'], error_message)
        else:
            try:
                self.send_text(msg['chat']['id'], "Photo received! 🌟 We're swiftly scanning it... Stay tuned for the magic! ✨")

                # Download the photo from telegram bot chat
                img_path = self.download_user_photo(msg)

                # Upload the photo to S3
                s3_url = self.upload_image_to_s3(img_path)

                # Send a request to yolo5 service for prediction
                yolo_results = self.request_yolo_prediction(s3_url)

                if len(yolo_results) == 1:
                    if yolo_results[0] == {'class': "", 'cx': 0, 'cy': 0, 'width': 0, 'height': 0}:
                        self.send_text(msg['chat']['id'], "Oops, your image has left me scratching my circuits! I must've missed a few updates. 😅 Could you send a different image, so I can try again?")
                        return

                 # Extract the 'labels' list which contains the detections
                detections = yolo_results['labels']

                # Create a dictionary to count occurrences of each class
                detection_counts = {}

                # Collect data for each detected object
                for item in detections:
                    class_name = item['class']
                    # Initialize the count for this class if not already done
                    if class_name not in detection_counts:
                        detection_counts[class_name] = 0

                    # Increment the count for the class
                    detection_counts[class_name] += 1

                # Now create a sentence for each class
                detection_descriptions = []
                for class_name, count in detection_counts.items():
                    if count == 1:
                        description = f"One {class_name} was detected.\n"
                    else:
                        description = f"{count} {class_name}s were detected.\n"

                    detection_descriptions.append(description)

                # Combine sentences into a summary paragraph
                summary = ''.join(detection_descriptions)

                # Send results to the telegram user
                self.send_text(msg['chat']['id'], f"We've scanned your image and here's what we found:\n{summary}")
                self.send_text(msg['chat']['id'],"One more surprise 🌟 Please wait ...")
                file_name = os.path.basename(img_path)
                new_filename = self.download_predicted_image_from_s3(file_name)
                self.send_photo(msg['chat']['id'], new_filename)
                self.send_text(msg['chat']['id'], "Exciting news! 🌟 A special gift 🎁 is on its way to you. Just a little more patience, and it'll be yours. It's worth the wait! 😊")
                prompt = summary
                image_url = self.dalle_generate_image(prompt)

                if image_url:
                    print("Image generated successfully.")
                    self.save_dalle_image(image_url, "generated_image.jpg")
                else:
                    print("Failed to generate image.")

                self.send_photo(msg['chat']['id'], "generated_image.jpg")
            except Exception as e:
                logger.error(e)

    def upload_image_to_s3(self, img_path):
        try:
            self.s3_resource.Bucket(self.Bucket_Name).put_object(
                Key=os.path.basename(img_path),
                Body=open(img_path, 'rb')
            )
        except Exception as e:
            logger.error(e)
            raise
            return
        #return f"https://{self.Bucket_Name}.s3.{self.aws_region}.amazonaws.com/{img_path}"
        return os.path.basename(img_path)

    def download_predicted_image_from_s3(self, file_name):
        s3_file_name = file_name.split('.')[0] + '_prediction.jpg'
        try:
            self.s3_resource.Bucket(self.Bucket_Name).download_file(
                s3_file_name,
                s3_file_name
            )

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                logger.error(f"The object does not exist.{e}")
            else:
                raise
                return
        return s3_file_name

    def request_yolo_prediction(self, s3_url):
        # Assuming you have an endpoint where YOLO5 service is running

        yolo_endpoint = 'http://yolo5:8081/predict'
        response = requests.post(yolo_endpoint, params={'imgName': s3_url})

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


