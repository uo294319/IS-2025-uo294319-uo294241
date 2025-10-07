import socket, sys


DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def encode_msg(msg):
    """Codifica el mensaje añadiéndole el fin de línea"""
    longitud  = "%d\n" % len(bytes(msg, "utf8"))
    return bytes(longitud + msg, "utf8")

def receive_msg(f):
    """Receives a message"""
    longitud = int(f.readline())
    msg = f.read(longitud)
    return msg

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # ----------------------------------------
    # ARGS

    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Uso: {sys.argv[0]} [ip] [puerto]")
        sys.exit(0)
        
    elif len(sys.argv) < 3:
        puerto = DEFAULT_PUERTO
        addr = DEFAULT_IP
        
    else:
        puerto = int(sys.argv[2], 10)
        addr = sys.argv[1]

    # ----------------------------------------
    # CLIENTE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, puerto))

    mensajes = [
        "ABC",
        "ABCD",
        "ABCDE"
    ]

    for mensaje in mensajes:

        mensaje = encode_msg(mensaje)

        if len(mensaje) > MAX_MSG_SIZE:
            print("El mensaje es demasiado largo (máx. 78 caracteres)")
            sys.exit(1)

        datagrama = s.sendall(mensaje)
        print(f"Mensaje enviado: {repr(mensaje)}")

    f = s.makefile(encoding="utf8", newline="\n")

    for mensaje in mensajes:
        mensaje = receive_msg(f)

        print(f"Mensaje recibido del servidor: '{repr(mensaje)}'")

    s.send(encode_msg("FINAL"))
    s.close()