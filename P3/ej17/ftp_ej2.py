import ftplib
import getpass

# Lista donde se guardarán las líneas recibidas del servidor
lista = []

def acumular(linea):
    lista.append(linea)

FTP_HOST = "localhost" 
FTP_USER = "uo294241"   

# Pedir la contraseña de forma segura
FTP_PASS = getpass.getpass("Contraseña: ")

try:
    # Conectar y autenticar
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print(f"Conectado a {FTP_HOST} como {FTP_USER}\n")

    # Cambiar a la carpeta de trabajo
    carpeta = "prueba-ftp"
    ftp.cwd(carpeta)
    print(f"Entrando en carpeta remota: {carpeta}\n")

    # Limpiar la lista
    lista = []

    # Ejecutar comando MLSD (formato estandarizado)
    respuesta = ftp.retrlines("MLSD", acumular)

    # Mostrar resultados crudos
    print("Respuesta del protocolo:", respuesta)
    print("\nContenidos de la carpeta remota (formato MLSD):")
    for l in lista:
        print("  ", l)

    ftp.quit()
    print("\nConexión cerrada correctamente.")

except ftplib.error_perm as e:
    print("El servidor no soporta MLSD o la carpeta no existe.")
    print("Error:", e)
except Exception as e:
    print("Error general:", e)
