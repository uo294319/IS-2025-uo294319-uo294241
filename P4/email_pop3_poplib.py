import poplib, getpass, os, sys

server="pop.gmail.com"

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2)

# Login
#username = input("Usuario: ")
username = "test.si2024.pl51@gmail.com"
password = os.getenv("PSSWD")
if not password:
    print("\nDale valor a la variable de entorno PSSWD")
    print("\tEjecuta: export PSSWD=<token>\n")
    sys.exit(1)

#Correo electronico
pop3_mail.user(username)
#Contraseña correo
pop3_mail.pass_(password) #Aquí iría la contraseña del correo
print(pop3_mail.retr(1)[1])
