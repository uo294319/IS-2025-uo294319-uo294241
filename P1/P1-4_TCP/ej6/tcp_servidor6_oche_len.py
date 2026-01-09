import socket, sys, time


DEFAULT_PUERTO = 9999
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# SERVIR CLIENTE
# ============================================================

def servir_cliente(sd, origen) -> None:
    """Atiende a un cliente conectado en el socket sd"""
    continuar = True
    # Bucle de atención al cliente conectado
    f = sd.makefile(encoding="utf8", newline="\n")

    while continuar:
        # Recibir el mensaje del cliente
        mensaje_len = int(f.readline())
        mensaje_str = f.read(mensaje_len)

        if mensaje_str=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif mensaje_str=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            # Darle la vuelta
            respuesta_str = mensaje_str[::-1]
            respuesta_len  = "%d\n" % len(bytes(respuesta_str, "utf8"))
            respuesta = str(respuesta_len)+respuesta_str

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            # Observa la transformación en bytes para enviarlo
            sd.sendall(bytes(respuesta, "utf8"))

            print(f"Cliente {origen[0]}:{origen[1]}: '{repr(("%d\n" % mensaje_len)+mensaje_str)}' -> '{repr(respuesta)}'")


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