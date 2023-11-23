#!/bin/bash

echo "Stopping all running Docker containers..."
docker stop $(docker ps -q)

echo "Deleting all Docker containers..."
docker rm $(docker ps -aq) -f

echo "Deleting all Docker images..."
docker rmi $(docker images -q) -f

echo "Deleting specific Docker networks..."
docker network rm docker_yolo_mongo_lanaNetwork docker_yolo_mongo_default lanaNetwork

echo "Listing all Docker containers (including exited ones)..."
docker ps -a

echo "Listing currently running Docker containers..."
docker container ls

echo "Listing Docker images..."
docker images ls

echo "Operations completed."
