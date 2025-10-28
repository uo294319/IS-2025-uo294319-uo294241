import getpass
import telnetlib
import time

HOST = "localhost"
tn = telnetlib.Telnet(HOST)
user = input("Enter your remote account: ")
password = getpass.getpass()

tn.read_until(b"login: ")
tn.write(user.encode('utf-8') + b"\n")
if password:
	tn.read_until(b"Password: ")
	tn.write(password.encode('utf-8') + b"\n")

tn.read_until(b"$")
tn.write(b"ps -ef  \n")

respuesta=tn.read_until(b"$").decode('utf-8')
print(respuesta)

if "udp_servidor3_con_ok.py" in respuesta:
	print("El servidor ya esta en ejecucion")
	tn.write(b"exit\n")
else:
	print("El servidor no esta en ejecucion, activando...")
	tn.write(b"nohup python3 udp_servidor3_con_ok.py & \n")
	time.sleep(1)
	tn.write(b"exit\n")

print(tn.read_all().decode('utf-8'))
