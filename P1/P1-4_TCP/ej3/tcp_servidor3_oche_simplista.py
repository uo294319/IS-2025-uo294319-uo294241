import socket, sys, time


DEFAULT_PUERTO = 9999
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def recvall(s , bufsize):
    i = 0
    mensaje = b""
    while i < bufsize:
            datos_recibidos = s.recv(bufsize)
            mensaje += datos_recibidos
            i = len(mensaje)

    return mensaje


def servir_cliente(sd, origen) -> None:
    """Atiende a un cliente conectado en el socket sd"""
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        # Recibir el mensaje del cliente
        mensaje_raw = sd.recv(MAX_MSG_SIZE)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        mensaje_str = str(mensaje_raw, "utf8")
        mensaje = mensaje_str[:-2]  # Quitar el "\r\n"

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
            respuesta_str = mensaje[::-1]+"\r\n"

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            # Observa la transformación en bytes para enviarlo
            sd.sendall(bytes(respuesta_str, "utf8"))

            print(f"Cliente {origen[0]}:{origen[1]}: '{repr(mensaje_str)}' -> '{repr(respuesta_str)}'")


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