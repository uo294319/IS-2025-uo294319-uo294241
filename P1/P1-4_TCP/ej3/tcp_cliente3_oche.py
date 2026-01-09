import socket, sys


DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"

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
        mensaje += "\r\n"  # Añadir el fin de línea
        mensaje_bytes = bytes(mensaje, "utf8")

        if len(mensaje_bytes) > MAX_MSG_SIZE:
            print("El mensaje es demasiado largo (máx. 78 caracteres)")
            sys.exit(1)

        datagrama = s.sendall(mensaje_bytes)

        print(f"Mensaje enviado al servidor: '{repr(mensaje)}'")

        respuesta_raw = s.recv(MAX_MSG_SIZE)
        respuesta_str = str(respuesta_raw, "utf8")

        print(f"Mensaje recibido del servidor: '{repr(respuesta_str)}'") 

    s.send(bytes("FINAL\r\n", "utf8"))
    s.close()
    