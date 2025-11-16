import ftplib
import getpass

FTP_HOST = "localhost"      
FTP_USER = "uo294241"    
FTP_PASS = getpass.getpass("Contraseña: ")

REMOTE_FILE = "prueba.txt"        # Nombre del archivo remoto
LOCAL_FILE = "prueba-copia.txt"   # Nombre con el que lo guardaremos localmente
REMOTE_DIR = "prueba-ftp"         # Carpeta remota donde está el archivo

try:
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print(f"Conectado al servidor {FTP_HOST} como {FTP_USER}")

    ftp.cwd(REMOTE_DIR)
    print(f"Directorio remoto: {REMOTE_DIR}")

    with open(LOCAL_FILE, "wb") as f_local:
        print(f"Descargando '{REMOTE_FILE}' → '{LOCAL_FILE}' ...")
        result = ftp.retrbinary(f"RETR {REMOTE_FILE}", f_local.write)

    print("Respuesta del servidor:", result)
    ftp.quit()
    print("Conexión cerrada correctamente.")

except ftplib.error_perm as e:
    print("Error de permisos o archivo inexistente:")
    print(e)
except FileNotFoundError:
    print("No se pudo crear el archivo local.")
except Exception as e:
    print("Error general:")
    print(e)
