# Use ubuntu as the base image
FROM ubuntu:jammy-20231004
#FROM ngrok/ngrok

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
# RUN apt-get install -y curl
# RUN apt-get install -y screen

# Upgrade pip
RUN pip install --upgrade pip
# RUN apt-get install -y net-tools lsof

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

## Download and install ngrok
#RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
#   tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
#  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
#   tee /etc/apt/sources.list.d/ngrok.list && \
#   apt update && apt install ngrok

# Set an environment variable for the ngrok token
# This assumes you will pass NGROK_TOKEN as a build argument
#ARG NGROK_TOKEN
#RUN ngrok config add-authtoken ${NGROK_TOKEN}
#RUN echo
#RUN ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app < /dev/null > /dev/null 2>&1 &
#RUN setsid ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app >/dev/null 2>&1 < /dev/null &
#RUN screen -dmS ngrok-session ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app
#RUN nohup ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app > /dev/null 2>&1 &
#RUN curl rapidly-rational-squirrel.ngrok-free.app

# Copy the rest of your application's source code
COPY . .

# Your application's default command to run
CMD ["python3", "app.py"]
