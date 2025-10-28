import paramiko
import base64
import time
import getpass
client = paramiko.SSHClient()

key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIGyv0Inha5y3967KYd58yuBCDR6aiRLBw64SQjM+APHB'))
client.get_host_keys().add('192.168.207.114', 'ssh-ed25519', key)

clave = getpass.getpass("Mete la clave: ")
client.connect('192.168.207.114', username='uo294319', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
