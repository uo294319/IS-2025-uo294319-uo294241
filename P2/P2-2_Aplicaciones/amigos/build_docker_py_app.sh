source ~/flaskenv/bin/activate
export DEPLOYMENT_MODE=development
export DATABASE_URI=mysql+pymysql://amigosuser:amigospass@172.18.0.2/amigosdb
#FLASK_APP=lanzar.py flask run -h 0.0.0.0
docker build -t ing_serv_amigos_fcm .