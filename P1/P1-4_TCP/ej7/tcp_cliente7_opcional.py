import socket, sys
import struct


DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5
MAX_MSG_SIZE = 80  # Incluyendo el "\r\n"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def encode_msg(msg):
    """Codifica el mensaje con su longitud al inicio."""
    msg = bytes(msg, "utf8")
    longitud = struct.pack(">H", len(msg))
    return longitud + msg



def receive_msg(s):
    """Recibe un mensaje codificado con su longitud al inicio."""
    # 1. Read the first 2 bytes (message length)
    raw_length = s.recv(2)
    
    # 2. Unpack the length (big-endian unsigned short)
    longitud = struct.unpack(">H", raw_length)[0]

    # 3. Read the rest of the message
    msg = s.recv(longitud)

    # 4. Decode from UTF-8 and return the message
    return msg.decode("utf8")

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


    for mensaje in mensajes:
        mensaje = receive_msg(s)

        print(f"Mensaje recibido del servidor: '{repr(mensaje)}'")

    s.send(encode_msg("FINAL"))
    s.close()