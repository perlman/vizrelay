FROM python:3.6

ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt

ENV RELAY_CONFIG config.json

ENTRYPOINT ["python", "main.py"]