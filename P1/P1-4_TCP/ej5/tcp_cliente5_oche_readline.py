import socket, sys


DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def recibe_mensaje(s) -> bytes:
    buffer = []
    terminator = [b"\r", b"\n"]

    while buffer[-2:] != terminator:
        buffer.append(s.recv(1))

    return b"".join(buffer) 

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
        mensaje += "\r\n"  # Añadir el fin de línea
        mensaje_bytes = bytes(mensaje, "utf8")

        if len(mensaje_bytes) > MAX_MSG_SIZE:
            print("El mensaje es demasiado largo (máx. 78 caracteres)")
            sys.exit(1)

        datagrama = s.sendall(mensaje_bytes)
        print(f"Mensaje enviado: {repr(mensaje)}")

    f = s.makefile(encoding="utf8", newline="\r\n")

    for mensaje in mensajes:
        respuesta_str = f.readline()

        print(f"Mensaje recibido del servidor: '{repr(respuesta_str)}'")

    s.send(bytes("FINAL\r\n", "utf8"))
    s.close()