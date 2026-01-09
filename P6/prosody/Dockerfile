FROM python:3.12
RUN pip install wheel slixmpp==1.8.6
WORKDIR /bot
COPY bot/bot_docker.py .
CMD ["python", "-u", "bot_docker.py"]