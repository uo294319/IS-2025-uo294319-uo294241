FROM python:3.12
RUN pip install flask gunicorn flask-sqlalchemy pymysql flask-migrate firebase-admin
RUN mkdir /amigos
COPY . /amigos
WORKDIR /amigos

EXPOSE 5000
CMD ["/usr/local/bin/gunicorn", "-R", "-b",  "0.0.0.0:5000", "-w", "4", "lanzar:app"]