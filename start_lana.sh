#!/bin/bash

# cd ~/PycharmProjects/docker_yolo_mongo

docker-compose up -d

if [ $? -ne 0 ]; then
    echo "Docker Compose failed to start. Exiting."
    exit 1
fi

echo "Docker-compose started successfully."

./start_Ngrok.sh
if [ $? -ne 0 ]; then
    echo "Failed to execute start_Ngrok.sh. Exiting."
    exit 1
fi