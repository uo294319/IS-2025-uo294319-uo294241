docker run --name amigos \
   -e DEPLOYMENT_MODE=production \
   -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
   -e PYTHONUNBUFFERED=1 \
   --rm -d --network pruebas ing_serv_amigos_fcm