import time
from pathlib import Path

import botocore
from flask import Flask, request
from detect import run
import uuid
import yaml
from loguru import logger
import os
import boto3
from pymongo import MongoClient

# Set Up Environment Variables :-
images_bucket = os.environ['BUCKET_NAME']
s3_access_key = os.environ['S3_ACCESS_KEY']
s3_secret_key = os.environ['S3_SECRET_KEY']

# mongodb_uri = 'mongodb://localhost:27017,localhost:27018,localhost:27019/' # os.environ['MONGODB_URI']
mongodb_uri = 'mongodb://mongo1:27017,mongo2:27018,mongo3:27019/'

# intialize S3 client
s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)

# Load Configuration from a YAML File :-
with open("data/coco128.yaml", "r") as stream:
    names = yaml.safe_load(stream)['names']

# Create a Flask Web Application :-
app = Flask(__name__)

# Define a Route for Predictions :-
@app.route('/predict', methods=['POST'])
def predict():
    # Generat a Unique ID for the Prediction :-
    # Generates a UUID for this current prediction HTTP request. This id can be used as a reference in logs to identify and track individual prediction requests.
    prediction_id = str(uuid.uuid4())

    # Log Information About the Prediction :-
    logger.info(f'prediction: {prediction_id}. start processing')

    # Receive Image Information from the Request :-
    # Receives a URL parameter representing the image to download from S3
    img_name = request.args.get('imgName')

    # Download the Image from S3 :-
    # TODO download img_name from S3, store the local image path in original_img_path
    #  The bucket name should be provided as an env var BUCKET_NAME.
    # original_img_path = f'/tmp/{img_name}'
    original_img_path = f'{img_name}'
    try:
        s3_client.download_file(images_bucket, img_name, original_img_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.error("The image does not found")
        else:
            logger.error(e)
            raise

    # Log Information About the Prediction :-
    logger.info(f'prediction: {prediction_id}/{original_img_path}. Download img completed')

    # Run the Object Detection on the Image :-
    # Predicts the objects in the image
    run(
        weights='yolov5s.pt',
        data='data/coco128.yaml',
        source=original_img_path,
        project='static/data',
        name=prediction_id,
        save_txt=True
    )
    # Log Completion of the Prediction Process :-
    logger.info(f'prediction: {prediction_id}/{original_img_path}. done')

    # This is the path for the predicted image with labels :-
    # The predicted image typically includes bounding boxes drawn around the detected objects, along with class labels and possibly confidence scores.
    predicted_img_path = Path(f'static/data/{prediction_id}/{original_img_path}')

    # Uplode Predicted image to S3 :-
    # TODO Uploads the predicted image (predicted_img_path) to S3 (be careful not to override the original image).
    s3_prediction_img_path = f'predictions/{img_name.split(".")[0]}_prediction.jpg'
    try:
        s3_client.upload_file(str(predicted_img_path), images_bucket, s3_prediction_img_path)
    except Exception as e:
        logger.error(e)
        raise
        return


    # Parse prediction labels and create a summary :-
    pred_summary_path = Path(f'static/data/{prediction_id}/labels/{original_img_path.split(".")[0]}.txt')
    if pred_summary_path.exists():
        with open(pred_summary_path) as f:
            labels = f.read().splitlines()
            labels = [line.split(' ') for line in labels]
            labels = [{
                'class': names[int(l[0])],
                'cx': float(l[1]),
                'cy': float(l[2]),
                'width': float(l[3]),
                'height': float(l[4]),
            } for l in labels]

        logger.info(f'prediction: {prediction_id}/{original_img_path}. prediction summary:\n\n{labels}')
        predicted_img_path = str(Path(f'static/data/{prediction_id}/{original_img_path}'))

        prediction_summary = {
            'prediction_id': prediction_id,
            'original_img_path': original_img_path,
            'predicted_img_path': predicted_img_path,
            'labels': labels,
            'time': time.time()
        }

        # Store the Prediction Summary in MongoDB :-
        # TODO store the prediction_summary in MongoDB
        # mongo_client = MongoClient(mongodb_uri)
        # mongo_client = MongoClient(mongodb_uri, replicaSet='myReplicaSet' )
        mongo_client = MongoClient(mongodb_uri)
        db = mongo_client['PSDB']
        collection = db['PSCollection']
        # collection.insert_one(prediction_summary)

        result = collection.insert_one(prediction_summary)  # Get the result of the insert operation
        prediction_summary["_id"] = str(result.inserted_id)  # Convert the ObjectId to a string



        mongo_client.close()
        #  Return the Prediction Summary as a Response :-
        return prediction_summary
    else:
        return f'prediction: {prediction_id}/{original_img_path}. prediction result not found', 404

# Start the Flask Application :-
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)