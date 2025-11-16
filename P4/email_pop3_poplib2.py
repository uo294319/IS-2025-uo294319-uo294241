import poplib, getpass, os, sys, email

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un
    # objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    # Si estas cabeceras contienen unicode hay que decodificarlas
    # lo que es un poco enrevesado
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    # Extraemos el cuerpo (este ya vendrá correctamente decodificado)
    cuerpo = msg.get_payload()

    # Pero si es multi-part, lo anterior nos retorna una lista
    # En ese caso nos quedamos con el primer elemento, que será a su
    # vez un mensaje con su propio payload
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + parte_1

    # Finalmente imprimimos un resumen, que son las cabeceras
    # extraidas y los primeros 200 caracteres del mensaje
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo)>500:
        print("...[omitido]")
    print("-"*80)

if __name__ == "__main__":
    server="pop.gmail.com"

    pop3_mail = poplib.POP3_SSL(server)
    pop3_mail.set_debuglevel(0)

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

    for i in range(pop3_mail.stat()[0]):
        _, lineas, _ = pop3_mail.retr(i+1)
        msg_bytes = b"\r\n".join(lineas)
        imprime_resumen_mensaje(msg_bytes)
