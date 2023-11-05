FROM ubuntu:jammy-20231004
WORKDIR /usr/src/app
ARG TOKEN

#RUN apt-get update
#RUN apt-get install -y python3
#RUN apt-get install -y python3-pip
#RUN pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
   tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
   echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
   tee /etc/apt/sources.list.d/ngrok.list && \
   apt update && apt install ngrok

RUN ngrok config add-authtoken ${TOKEN}
#RUN ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app > /dev/null 2>&1 &
#RUN nohup ngrok http 8443 --domain rapidly-rational-squirrel.ngrok-free.app &

COPY . .

CMD ["python3", "app.py"]
