import socket, sys, time


DEFAULT_PUERTO = 9999
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def encode_msg(msg):
    """Codifica el mensaje añadiéndole el fin de línea"""
    return bytes(msg + "\r\n", "utf8")

def decode_msg(msg):
    """Decodifica el mensaje quitándole el fin de línea"""
    return str(msg, "utf8")[:-2]

def recvall(s , bufsize):
    i = 0
    mensaje = b""
    while i < bufsize:
            datos_recibidos = s.recv(bufsize)
            mensaje += datos_recibidos
            i = len(mensaje)

    return mensaje

def recibe_mensaje(s) -> str:
    buffer = []
    terminator = [b"\r", b"\n"]

    while buffer[-2:] != terminator:
        buffer.append(s.recv(1))

    return b"".join(buffer)


# ============================================================
# SERVIR CLIENTE
# ============================================================

def servir_cliente(sd, origen) -> None:
    """Atiende a un cliente conectado en el socket sd"""
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        # Recibir el mensaje del cliente
        mensaje = recibe_mensaje(sd)
        mensaje = decode_msg(mensaje)  # Quitarle el "\r\n"

        if mensaje=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif mensaje=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            # Darle la vuelta
            respuesta = mensaje[::-1]

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            # Observa la transformación en bytes para enviarlo
            sd.sendall(encode_msg(mensaje[::-1]))

            print(f"Cliente {origen[0]}:{origen[1]}: '{repr(mensaje)}' -> '{repr(respuesta)}'")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # ----------------------------------------
    # ARGS

    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Uso: {sys.argv[0]} [puerto]")
        sys.exit(0)

    elif len(sys.argv) < 3:
        puerto = DEFAULT_PUERTO
        
    else:
        puerto = int(sys.argv[1],10)

    # ----------------------------------------
    # SERVIDOR

    # Crear el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

    # Asignarle puerto
    s.bind(("", puerto))

    # Ponerlo en modo pasivo
    s.listen(5)  # Máximo de clientes en la cola de espera al accept()

    # Bucle principal de espera por clientes
    while True:
        print("Esperando un cliente")
        sd, origen = s.accept()
        print("Nuevo cliente conectado desde %s, %d" % origen)

        time.sleep(1) # Retardo

        servir_cliente(sd, origen)