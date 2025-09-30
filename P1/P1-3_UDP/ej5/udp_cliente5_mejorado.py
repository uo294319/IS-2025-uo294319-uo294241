import socket
import sys
import uuid
import json

if len(sys.argv) < 3:
    puerto = 9999
    addr = "127.0.0.1"
else:
    addr = sys.argv[1]
    puerto = int(sys.argv[2], 10)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

aux = 1
mensaje = input("Mensaje: ")
var = 0.1

while "FIN" not in mensaje:
    id_mensaje = str(uuid.uuid4())
    paquete = {
        "id": id_mensaje,
        "contenido": f"{aux}: {mensaje}"
    }

    s.sendto(json.dumps(paquete).encode("utf-8"), (addr, puerto))
    s.settimeout(var)

    while var <= 2.0:
        try:
            resp, origen = s.recvfrom(1024)
            respuesta = json.loads(resp.decode("utf-8"))

            if respuesta.get("estado") == "OK" and respuesta.get("id") == id_mensaje:
                print("Recibido")
                aux += 1
                mensaje = input("Mensaje: ")
                var = 0.1
                break
            else:
                print("ERROR")
        except socket.timeout:
            print("TIMEOUT")
            s.sendto(json.dumps(paquete).encode("utf-8"), (addr, puerto))
            var *= 2
            s.settimeout(var)

    else:
        exit()

s.close()
