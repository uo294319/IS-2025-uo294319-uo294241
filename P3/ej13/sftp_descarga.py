import paramiko, getpass, base64, sys
from stat import S_ISDIR

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
print("Se copiaran unos ficheros...")
#Abrir canal sftp
sftp = cliente.open_sftp()

directorio=sftp.listdir()
i = 0
nombre_nuevo = " "
for fichero in directorio:
	#Comprar si es fichero 
	if not S_ISDIR(sftp.stat(fichero).st_mode):
		nombre_nuevo = "fichero_" + str(i)
		print("Copiando fichero", fichero, "en", nombre_nuevo)
		sftp.get(fichero, nombre_nuevo)
		i = i + 1
print("Copia realizada con exito!")
