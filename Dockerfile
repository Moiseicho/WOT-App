FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y xvfb

ENV DISPLAY=:99

CMD ["Xvfb", ":99", "-ac", "-screen", "0", "1280x1024x16"]

RUN apt-get update && apt-get install -y \
    curl \
    &&  apt-get install -y python3 python3-pip python3-tk && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY WebsiteChecker.py front.py api.py main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["xvfb-run", "python", "main.py"]

