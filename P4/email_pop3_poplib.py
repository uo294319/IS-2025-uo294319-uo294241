import poplib
import os
import sys

# Configuración del servidor
server = "pop.gmail.com"

# 1. Instanciar el objeto y activar depuración
print("--- Conectando al servidor ---")
pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2)

# Configuración de credenciales
username = "test.si2024.pl51@gmail.com"
password = os.getenv("PSSWD")

# Verificación de seguridad básica para la variable de entorno
if not password:
    print("\n[ERROR] Dale valor a la variable de entorno PSSWD")
    print("\tLinux/Mac: export PSSWD='tu_token_o_contraseña'")
    print("\tWindows (CMD): set PSSWD=tu_token_o_contraseña")
    print("\tWindows (PowerShell): $env:PSSWD='tu_token_o_contraseña'\n")
    sys.exit(1)

try:
    # 2. Enviar usuario y contraseña
    pop3_mail.user(username)
    pop3_mail.pass_(password)

    # 3. Obtener el número de mensajes para evitar errores si el buzón está vacío
    # stat() devuelve (número de mensajes, tamaño total)
    num_messages = len(pop3_mail.list()[1])
    
    if num_messages > 0:
        print(f"\n--- Recuperando mensaje 1 de {num_messages} ---")
        
        # 4. Recuperar el primer mensaje usando retr(1)
        # retr() retorna una tupla: (respuesta, lista_de_lineas, octetos)
        respuesta_servidor, lista_lineas, tamano = pop3_mail.retr(1)
        
        # 5. Mostrar el contenido tal como poplib lo devuelve (lista de bytes)
        print("Contenido crudo (lista de líneas):")
        print(lista_lineas)
    else:
        print("El buzón está vacío, no se puede recuperar el mensaje 1.")

except poplib.error_proto as e:
    print(f"Ocurrió un error de protocolo: {e}")

finally:
    # Cerrar la conexión limpiamente
    pop3_mail.quit()
    print("\n--- Conexión cerrada ---")