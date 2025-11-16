import ftplib
import getpass

# Lista donde se guardarán las líneas recibidas del servidor
lista = []

# Callback que acumula las líneas recibidas por el comando LIST
def acumular(linea):
    lista.append(linea)

FTP_HOST = "localhost" 
FTP_USER = "uo294241"

FTP_PASS = getpass.getpass("Contraseña: ")

try:
    # Conectar al servidor FTP
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print(f"Conectado al servidor {FTP_HOST} como {FTP_USER}\n")

    # Cambiar de directorio remoto (debe existir)
    carpeta = "prueba-ftp"
    ftp.cwd(carpeta)
    print(f"Entrando en carpeta remota: {carpeta}\n")

    lista = []

    # Ejecutar LIST y acumular resultado mediante el callback
    respuesta = ftp.retrlines("LIST", acumular)

    # Mostrar resultados
    print("Respuesta del protocolo:", respuesta)
    print("\nContenidos de la carpeta remota:")
    for l in lista:
        print("  ", l)

    # Cerrar conexión
    ftp.quit()
    print("\nConexión cerrada correctamente.")

except ftplib.all_errors as e:
    print("Error al conectar o ejecutar comando FTP:")
    print(e)
