import firebase_admin
from firebase_admin import credentials, messaging
import os

# Variable global para las credenciales
cred = None

try:
    # Construimos la ruta al archivo serviceAccount.json.
    # Se asume que está en la misma carpeta que este fichero (app/)
    base_path = os.path.dirname(__file__)
    json_path = os.path.join(base_path, "serviceAccount.json")
    
    # Inicializamos la app de Firebase
    cred_obj = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred_obj)
    cred = cred_obj
    print(f"FCM: Inicializado correctamente usando {json_path}")
except Exception as e:
    print(f"FCM: Error al inicializar: {e}")
    cred = None

def notificar_amigos(tokens, body):
    """
    Envía una notificación multicast a la lista de tokens proporcionada.
    """
    if cred is None:
        print("FCM: No se envia notificacion (credenciales no cargadas)")
        return

    if not tokens:
        print("FCM: No hay tokens de dispositivo para notificar")
        return

    try:
        # Creamos el payload de la notificación
        notification_payload = messaging.Notification(
            title="Amigos",
            body=body
        )

        # Creamos el mensaje multicast
        message = messaging.MulticastMessage(
            notification=notification_payload,
            tokens=tokens
        )

        print(f"FCM: Enviando notificacion '{body}' a {len(tokens)} dispositivos...")
        response = messaging.send_each_for_multicast(message)
        print(f"FCM: Envio finalizado. Exitos: {response.success_count}, Fallos: {response.failure_count}")
        
    except Exception as e:
        print(f"FCM: Excepción al enviar mensaje: {e}")