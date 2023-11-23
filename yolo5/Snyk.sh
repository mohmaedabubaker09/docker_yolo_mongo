#!/bin/bash

# snyk container test mohamedabubaker09/lana_yolo5:ultralytics-yolov5-latest-cpu --file=Dockerfile

snyk container test mohamedabubaker09/lana_yolo5:ultralytics-yolov5-latest-cpu --file=Dockerfile > ~/PycharmProjects/docker_yolo_mongo/yolo5/snyk-scan-results/lana_yolo5-ultralytics-yolov5-latest-cpu_before.txt

