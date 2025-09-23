import socket, sys

DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5

if "-h" in sys.argv or "--help" in sys.argv:
    print(f"Uso: {sys.argv[0]} [ip] [puerto]")
    sys.exit(0)
	
elif len(sys.argv) < 3:
	puerto = DEFAULT_PUERTO
	addr = DEFAULT_IP
	
else:
	puerto = int(sys.argv[2], 10)
	addr = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((addr, puerto))

mensaje = "ABCDE"
for i in range(NUM_REPS):
	datagrama = s.send(mensaje.encode("utf-8"))
	
mensaje = "FINAL"
datagrama = s.send(mensaje.encode("utf-8"))

s.close()