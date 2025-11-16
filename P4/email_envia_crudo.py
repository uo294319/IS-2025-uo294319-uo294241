import socket
import sys


def RecvReply(sock, code):
    """
    Recibe hasta 1024 bytes del socket, imprime lo recibido y verifica
    que los primeros tres bytes coincidan con el código (bytes) pasado.
    En caso contrario muestra error y termina el programa.
    """
    reply = sock.recv(1024)
    if not reply:
        print("No se recibió respuesta del servidor.")
        sys.exit(1)
    # Imprimir la respuesta para depuración (decodificando si es posible)
    try:
        print("Servidor:", reply.decode().rstrip())
    except Exception:
        print("Servidor (bytes):", reply)

    # Verificar el código
    if reply[:3] != code:
        print(f"Error: código esperado {code!r}, recibido {reply[:3]!r}")
        sys.exit(1)

if __name__ == '__main__':
    # Configurar aquí tus datos (modifica fromaddr y toaddr por tu cuenta en uniovi)
    server = 'relay.uniovi.es'
    port = 25
    fromaddr = 'uo294241@uniovi.es'
    toaddr   = 'uo294319@uniovi.es'
    subject = 'Hola'
    data = 'Soy el fantasma de las navidades pasadas.'

    # Construir el message según la especificación (cabeceras + cuerpo)
    message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

    # Crear socket TCP y conectar al servidor SMTP
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((server, port))
    except Exception as e:
        print("Error al conectar con el servidor:", e)
        sys.exit(1)

    try:
        # Recibir saludo inicial 220
        RecvReply(clientSocket, b'220') # 220 Indica que el servicio está listo

        # HELO
        hostname = socket.gethostname()
        cmd = f'HELO {hostname}\r\n'.encode()
        clientSocket.sendall(cmd)
        RecvReply(clientSocket, b'250') # 250 OK

        # MAIL FROM
        cmd = f'MAIL FROM:<{fromaddr}>\r\n'.encode()
        clientSocket.sendall(cmd)
        RecvReply(clientSocket, b'250') # 250 OK

        # RCPT TO
        cmd = f'RCPT TO:<{toaddr}>\r\n'.encode()
        clientSocket.sendall(cmd)
        RecvReply(clientSocket, b'250') # 250 OK

        # DATA
        cmd = 'DATA\r\n'.encode()
        clientSocket.sendall(cmd)
        RecvReply(clientSocket, b'354') # 354 Listo para recibir datos

        # Enviar el mensaje (cabeceras + cuerpo + terminador \r\n.\r\n)
        clientSocket.sendall(message.encode())
        RecvReply(clientSocket, b'250') # 250 OK, mensaje recibido

        # QUIT
        cmd = 'QUIT\r\n'.encode()
        clientSocket.sendall(cmd)
        RecvReply(clientSocket, b'221') # 221 Cerrando conexión

    finally:
        clientSocket.close()