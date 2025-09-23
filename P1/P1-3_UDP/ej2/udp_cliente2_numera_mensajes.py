import socket, sys

if len(sys.argv) < 3:
	puerto=9999
	addr="127.0.0.1"
else:
	puerto= int(sys.argv[2],10)
	addr = sys.argv[1]
 
socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socket.connect((addr,puerto))
aux = 1
mensaje=str(aux) +": " + input("")

while mensaje != "FIN":
	datagrama = socket.sendto(mensaje.encode("utf-8"),(addr,puerto))
	OK, origen =socket.recvfrom(1024)
	print(OK.decode("utf-8"))
	aux += 1
	mensaje = str(aux) + ": " + input("")

