import socket, sys, os, ssl

def RecvReply(sock):
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
    code = b"+OK"
    if reply[:3] != code:
        print(f"Error: código esperado {code!r}, recibido {reply[:3]!r}")
        sys.exit(1)

    return reply


if __name__  == "__main__":

    server = "pop.gmail.com"
    port=995

    # Login
    #username = input("Usuario: ")
    username = "test.si2024.pl51@gmail.com"
    password = os.getenv("PSSWD")

    s = socket.socket()
    s.connect((server, port))
    context = ssl.create_default_context()
    sc = context.wrap_socket(s, server_hostname=server)

    RecvReply(sc)

    # Usuario y PASSWD
    sc.sendall(f"USER {username}\r\n".encode("utf-8"))
    RecvReply(sc)
    sc.sendall(f"PASS {password}\r\n".encode("utf-8"))
    RecvReply(sc)

    # STAT
    sc.sendall(b"STAT\r\n")
    n_correos = RecvReply(sc).decode("utf-8").split(" ")[1]

    # RETR
    sc.sendall("RETR 1\r\n".encode("utf-8"))
    RecvReply(sc)

    msg = b""
    while msg[-5:] != b"\r\n.\r\n":
        msg += sc.recv(1)

    msg = msg.decode("utf-8")
    print(msg)

    for line in msg.split("\n"):
        if "Subject:" in line or "From:" in line:
            print(line)