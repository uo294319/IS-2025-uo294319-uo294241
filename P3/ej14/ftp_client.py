from ftplib import FTP
import getpass

# Configura tus datos
FTP_SERVER = "localhost"   
FTP_USER = "uo294241"
FTP_PASS = getpass.getpass('Contraseña: ')

# Conexión al servidor FTP
ftp = FTP(FTP_SERVER)
ftp.login(FTP_USER, FTP_PASS)

print("Conectado a:", FTP_SERVER)
print("Contenido del directorio raíz:")
ftp.retrlines('LIST')

# Crear carpeta remota
folder_name = "prueba-ftp"
try:
    ftp.mkd(folder_name)
    print(f"Carpeta '{folder_name}' creada.")
except:
    print(f"La carpeta '{folder_name}' ya existe.")

# Cambiar a la carpeta
ftp.cwd(folder_name)

# Subir un archivo
file_path = "ejemplo.py" 
with open(file_path, "rb") as f:
    ftp.storbinary(f"STOR {file_path}", f)
    print(f"Archivo '{file_path}' subido correctamente.")

# Descargar un archivo del servidor
download_name = "descargado.py"
with open(download_name, "wb") as f:
    ftp.retrbinary(f"RETR ejemplo.py", f.write)
    print(f"Archivo descargado como '{download_name}'.")

ftp.quit()
print("Conexión cerrada.")
