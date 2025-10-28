import paramiko, getpass, base64, sys

ip_remota=None
usuario=None
if len(sys.argv) == 3:
	usuario = sys.argv[1]
	ip_remota = sys.argv[2]
else:
	ip_remota = 'localhost'
	usuario = 'uo294241'

cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Se realizara una conexión a ", ip_remota, "con el usuario:", usuario)
password_usuario = getpass.getpass("Contraseña: ")
cliente.connect(ip_remota, username=usuario, password=password_usuario)

print("-> Conexion establecida <-")

#Abrir un canal sftp
sftp = cliente.open_sftp()

listado = sftp.listdir()
for nombre in listado:
    print(nombre)
