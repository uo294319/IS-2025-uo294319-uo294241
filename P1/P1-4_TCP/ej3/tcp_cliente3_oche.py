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
    return bytes(msg + "\r\n", "utf8")

def decode_msg(msg):
    """Decodifica el mensaje quitándole el fin de línea"""
    return str(msg, "utf8")[:-2]


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
        "Hola, servidor",
        "¿Cómo estás?",
        "Este es un mensaje de prueba",
        "Otro mensaje",
        "Adiós"
    ]

    for mensaje in mensajes:
        mensaje = encode_msg(mensaje)

        if len(mensaje) > MAX_MSG_SIZE:
            print("El mensaje es demasiado largo (máx. 78 caracteres)")
            sys.exit(1)

        datagrama = s.sendall(mensaje)

        mensaje = s.recv(MAX_MSG_SIZE)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        mensaje = str(mensaje, "utf8")

        print(f"Mensaje recibido del servidor: '{mensaje[:-2]}'")  # Quitarle el "\r\n"

    s.send(encode_msg("FINAL"))
    s.close()