import socket, sys
import struct


DEFAULT_PUERTO = 9999
DEFAULT_IP = "127.0.0.1"
NUM_REPS = 5
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

    for mensaje_str in mensajes:

        mensaje_bytes = encode_msg(mensaje_str)

        if len(mensaje_bytes) > MAX_MSG_SIZE:
            print("El mensaje es demasiado largo (máx. 78 caracteres)")
            sys.exit(1)

        datagrama = s.sendall(mensaje_bytes)
        print(f"Mensaje enviado:\t{repr(mensaje_bytes)}  \t(original: '{mensaje_str}')")


    for mensaje in mensajes:
        respuesta_bytes, respuesta_str = receive_msg(s)

        print(f"Mensaje recibido:\t'{repr(respuesta_bytes)}  \t(original: '{respuesta_str}')")

    s.send(encode_msg("FINAL"))
    s.close()