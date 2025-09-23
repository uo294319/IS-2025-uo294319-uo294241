import socket, sys

if len(sys.argv) < 2:
	puerto = 9999
else:
	puerto = int(sys.argv[1], 10)

print("Puerto: ", puerto)
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("" , puerto))
while True:
	datagrama, origen = socket.recvfrom(1024)
	print("Dirección de origen: ", origen)
	print("Contenido: ", datagrama.decode("utf-8"))
	socket.sendto(datagrama, origen)
