FROM python:3.9-slim-buster

WORKDIR /app

COPY api.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api.py"]

