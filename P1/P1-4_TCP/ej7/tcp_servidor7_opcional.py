import socket, sys, time
import struct

DEFAULT_PUERTO = 9999
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def encode_msg(msg) -> bytes:
    """Codifica el mensaje con su longitud al inicio."""
    msg = bytes(msg, "utf8")
    longitud = struct.pack(">H", len(msg))
    return longitud + msg



def receive_msg(s) -> tuple[bytes, str]:
    """Recibe un mensaje codificado con su longitud al inicio."""
    # 1. Read the first 2 bytes (message length)
    raw_length = s.recv(2)
    
    # 2. Unpack the length (big-endian unsigned short)
    longitud = struct.unpack(">H", raw_length)[0]

    # 3. Read the rest of the message
    msg = s.recv(longitud)

    # 4. Decode from UTF-8 and return the message
    return raw_length + msg, msg.decode("utf8")


# ============================================================
# SERVIR CLIENTE
# ============================================================

def servir_cliente(sd, origen) -> None:
    """Atiende a un cliente conectado en el socket sd"""
    continuar = True
    # Bucle de atención al cliente conectado

    while continuar:
        # Recibir el mensaje del cliente
        mensaje_bytes, mensaje_str = receive_msg(sd)

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
            respuesta_bytes = encode_msg(respuesta_str)

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            # Observa la transformación en bytes para enviarlo
            sd.sendall(respuesta_bytes)

            print(f"Cliente {origen[0]}:{origen[1]}: '{repr(mensaje_bytes)}' -> '{repr(respuesta_bytes)}'")


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