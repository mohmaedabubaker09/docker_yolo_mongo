#!/bin/bash

snyk container test mohamedabubaker09/lana_bot:ubuntu-jammy-20231004 --file=Dockerfile > ~/PycharmProjects/docker_yolo_mongo/lanabot/snyk-scan-results/lana_bot:ubuntu-jammy-20231004_before.txt
