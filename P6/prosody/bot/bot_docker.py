import slixmpp          # Biblioteca principal para XMPP
import asyncio         # Para manejar operaciones asíncronas
import logging          # Para el log de depuración
import getpass          # Para pedir la contraseña de forma segura
import os               # Para obtener variables de entorno (contraseña, para docker)
import ssl              # Para manejar certificados SSL

# CONSTANTES
JID = "bot@ingserv123"
IP_DEFAULT = "localhost"
PORT = 5222
ENV_CLAVE = "CLAVEBOT"
ENV_IP = "IP_SERVIDOR"
CERT_FILE = "../etc/prosody/certs/ingserv123.crt"

# Esta es la sintaxis de herencia en Python
class MyBot(slixmpp.ClientXMPP):
    # El constructor vuelve a su forma original.
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.register_plugin('xep_0085')

        # Registrar los eventos y sus manejadores
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

        self.add_event_handler("chatstate_active", self.on_active)
        self.add_event_handler("chatstate_composing", self.on_composing)
        self.add_event_handler("chatstate_paused", self.on_paused)
        self.add_event_handler("chatstate_inactive", self.on_inactive)

    # Implementación de los callbacks (todos son tipo async)
    async def callback_para_session_start(self, event):
        print("Sesión iniciada!")
        self.send_presence() # Staza de presencia Online
        
        # get_roster() es una corutina por lo que hay que usar 'await'
        await self.get_roster() # Obtener el roster
        print("Roster recibido.")

    async def callback_para_message(self, event):
        recibido = event['body']
        print(f"Recibido un mensaje de tipo {event['type']} de {event['from']}")
        print(f"Que dice: {recibido}")

        if event["type"] == "chat":
            msg = self.Message()
            msg["to"] = event["from"]
            msg["type"] = "chat"
            msg["chat_state"] = "active"

            if recibido.startswith("="):
                expresion = recibido[1:] 

                try:
                    resultado = eval(expresion)
                    msg["body"] = str(resultado)

                except Exception as e:
                    msg["body"] = f"Error al calcular: {e}"
            else:
                # Si no es fórmula, hacemos el ECO del Ejercicio 7
                msg["body"] = "¿" + recibido + "?"
            
            msg.send()

    async def on_composing(self, event):
        print(f"{event['from'].bare} está escribiendo...")

    async def on_paused(self, event):
        print(f"{event['from'].bare} ha parado de escribir")

    async def on_active(self, event):
        print(f"{event['from'].bare} está activo")

    async def on_inactive(self, event):
        print(f"{event['from'].bare} está inactivo")

# Programa principal
if __name__ == "__main__":
    # Depuración
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    # Obtener credenciales
    
    clave = os.environ.get(ENV_CLAVE)
    if clave is None:
        clave = getpass.getpass("Contraseña: ")

    # Manejo del certificado. Hay que extraer una copia de la que se generó
    # en el servidor
    cert_file = CERT_FILE
    ssl_context = ssl.create_default_context()

    if os.path.exists(cert_file):
        print(f"Cargando certificado de confianza desde: {cert_file}")
        ssl_context.load_verify_locations(cert_file)
        
        # Desactivar la comprobación del nombre de host.
        # Esto es necesario porque el certificado es para 'ingservXX' pero conectamos a 'localhost'.
        print("Desactivando la comprobación de hostname.")
        ssl_context.check_hostname = False
    else:
        # Incluso podemos confiar ciegamente en el certificado, sin tener uno instalado en el cliente
        print(f"ADVERTENCIA: No se encontró '{cert_file}'. Desactivando TODA la validación de certificado.")
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    # Instanciar el bot
    client = MyBot(JID, clave)

    # Asignar el contexto SSL a la instancia del cliente
    client.ssl_context = ssl_context
    # Completar con registro del plugin
    
    # Conectar el bot al servidor
    ip = os.environ.get(ENV_IP, IP_DEFAULT)
    client.connect((ip, PORT))
    
    # Iniciar el bucle de eventos.
    client.process(forever=True)
