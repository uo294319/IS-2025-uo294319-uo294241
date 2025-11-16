import ftplib
import getpass
import os

FTP_HOST = "localhost"      
FTP_USER = "uo294241"    
FTP_PASS = getpass.getpass("Contraseña: ")

REMOTE_DIR = "prueba-ftp"  

try:
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print(f"Conectado al servidor {FTP_HOST} como {FTP_USER}")

    ftp.cwd(REMOTE_DIR)
    print(f"Directorio remoto: {REMOTE_DIR}")

    print("Obteniendo lista de archivos...")
    elementos = list(ftp.mlsd())

    for nombre, datos in elementos:
        tipo = datos.get("type", "")
        if tipo == "file":
            print(f"Descargando archivo: {nombre} ...")
            with open(nombre, "wb") as f_local:
                ftp.retrbinary(f"RETR {nombre}", f_local.write)
            print(f"Guardado localmente como: {nombre}")
        else:
            print(f"Ignorado (no es archivo): {nombre}")

    ftp.quit()
    print("Conexión cerrada correctamente.")

except ftplib.error_perm as e:
    print("Error de permisos o acceso:")
    print(e)
except FileNotFoundError:
    print("No se pudo crear el archivo local.")
except Exception as e:
    print("Error general:")
    print(e)
