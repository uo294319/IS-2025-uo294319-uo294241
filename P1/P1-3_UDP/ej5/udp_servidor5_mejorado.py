import socket
import sys
import random
import json

if len(sys.argv) < 2:
    puerto = 9999
else:
    puerto = int(sys.argv[1], 10)

print("Puerto:", puerto)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", puerto))

procesados = set()

while True:
    data, origen = sock.recvfrom(1024)

    try:
        mensaje = json.loads(data.decode("utf-8"))
        id_mensaje = mensaje["id"]
        contenido = mensaje["contenido"]
    except:
        print("ERROR")
        continue

    if random.randint(0, 10) <= 5:
        print("Simulando paquete perdido")
        continue

    if id_mensaje in procesados:
        print(f"Duplicado recibido con el ID: {id_mensaje}")
    else:
        print(f"Dirección de origen: {origen}")
        print(f"ID: {id_mensaje}")
        print(f"Contenido: {contenido}")
        procesados.add(id_mensaje)

    respuesta = {"estado": "OK", "id": id_mensaje}
    sock.sendto(json.dumps(respuesta).encode("utf-8"), origen)
