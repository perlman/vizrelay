FROM python:3.6
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app
EXPOSE 5000

ENV RELAY_CONFIG_JSON {}
ENV RELAY_CONFIG_FILE config.json

ENTRYPOINT ["/app/entry-point.sh"]
CMD ["python", "main.py"]