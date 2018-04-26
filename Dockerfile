FROM python:3.6

ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt

ENV RELAY_CONFIG_JSON {}
ENV RELAY_CONFIG_FILE config.json

ENTRYPOINT ["/app/entry-point.sh"]
CMD ["python3", "main.py"]