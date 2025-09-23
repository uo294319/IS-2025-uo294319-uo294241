import socket

puerto = 12345
print("Puerto:", puerto)
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("" , puerto))
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

while True:
	datagrama, origen = servidor.recvfrom(1024)
	msg_broadcast = datagrama.decode("utf-8")
	if msg_broadcast == "BUSCANDO HOLA":
		servidor.sendto(b"RESPUESTA", origen)
	elif msg_broadcast == "HOLA":
		mensaje_servidor = "HOLA: " + origen[0]
		print(mensaje_servidor)
		servidor.sendto(mensaje_servidor.encode("utf-8"), origen)
