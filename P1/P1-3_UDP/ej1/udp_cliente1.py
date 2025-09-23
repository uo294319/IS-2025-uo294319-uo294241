import socket, sys

if len(sys.argv) < 3:
	puerto = 9999
	addr = "127.0.0.1"
else:
	puerto = int(sys.argv[2],10)
	addr = sys.argv[1]

socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socket.connect((addr,puerto))
mensaje = input("--> ")
while mensaje != "FIN":
	datagrama = socket.sendto(mensaje.encode("utf-8"),(addr,puerto))
	mensaje=input("--> ")

socket.close()