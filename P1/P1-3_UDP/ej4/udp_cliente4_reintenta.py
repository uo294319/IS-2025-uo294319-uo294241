import socket, sys

if len(sys.argv) < 3:
	puerto = 9999
	addr = "127.0.0.1"
else:
	puerto = int(sys.argv[2],10)
	addr = sys.argv[1]

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((addr,puerto))

aux = 1
mensaje = str(aux) + ": " + input("")
var = 0.1
while  not "FIN" in mensaje:
	s.sendto(mensaje.encode("utf-8"),(addr,puerto))
	s.settimeout(var)
	while var <= 2.0 and not "FIN" in mensaje:
		try:
			respuesta, origen = s.recvfrom(1024)
			print (respuesta.decode("utf-8"))
			print ("Introduzca el mensaje: ")
			aux = aux + 1
			mensaje = str(aux) + ": " + input("")
		except  socket.timeout:
			s.sendto(mensaje.encode("utf-8"),(addr,puerto))
			var = var *2
			s.settimeout(var)
	if("FIN" in mensaje):
		print("Se ha introducido FIN")
		exit()
	else:
		print("Puede que el servidor esté caído. Inténtelo más tarde")
		exit()

s.close()
