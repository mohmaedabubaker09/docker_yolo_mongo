FROM ubuntu:jammy-20231004
# FROM python:3.11.4-slim

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
# RUN apt-get install -y curl
# RUN apt-get install -y screen

RUN pip install --upgrade pip
# RUN apt-get install -y net-tools lsof

COPY requirements.txt .

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

## Download and install ngrok
#RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
#   tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
#  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
#   tee /etc/apt/sources.list.d/ngrok.list && \
#   apt update && apt install ngrok

# Copy the rest of your application's source code
COPY . .

CMD ["python3", "app.py"]
