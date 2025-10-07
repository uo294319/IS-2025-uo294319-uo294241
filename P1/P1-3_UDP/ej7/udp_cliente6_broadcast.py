import socket, sys

if len(sys.argv) < 2:
	addr = "127.0.0.1"
else:
	addr = sys.argv[1]

puerto = 12345
cliente = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
var = 2

msg_broadcast = "BUSCANDO HOLA"
checksum = cliente.sendto(msg_broadcast.encode("utf-8"),(addr, puerto))
if checksum > 0:
	print("Broadcast enviado con éxito ")
else:
	print("Broadcast falló al enviar ")

direccion_serv = None
while True:
	cliente.settimeout(var)
	try:
		respuesta_servidor, origen = cliente.recvfrom(1024)
		if respuesta_servidor.decode("utf-8") == "RESPUESTA":
			if direccion_serv == None:
				direccion_serv = origen
			print("Recibida respuesta desde la dirección: ", origen[0])
	except socket.timeout:
		print("ERROR")
		break

if direccion_serv == None:
	print("No hay respuesta")
	sys.exit()

cliente.sendto(b"HOLA", direccion_serv)
respuesta_servidor, direccion_serv = cliente.recvfrom(1024)
if respuesta_servidor[0:4].decode("utf-8") == "HOLA":
	print("Respuesta desde el servidor: ", direccion_serv[0])
	print("Mensaje: ", respuesta_servidor.decode("utf-8"))
	print("FIN")
	sys.exit()

cliente.close()