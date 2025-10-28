import paramiko
import base64
import time
import getpass
client = paramiko.SSHClient()

key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAILxCP9CzQ3MZ6NIaTw5WVqT6i7lf0r2mDE1dmeyzuns0'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

clave = getpass.getpass("Mete la clave: ")
client.connect('localhost', username='uo294241', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
