import firebase_admin
from firebase_admin import credentials, messaging

# Cargar credenciales desde el archivo JSON obtenido de Firebase
json_secrets = "serviceAccount.json"
cred = credentials.Certificate(json_secrets)
firebase_admin.initialize_app(cred)

fcm_token = input("Token de dispositivo: ")
notification_title = "Hola desde Python!"
notification_body = "Este mensaje ha sido enviado desde firebase-admin"

try:
    notification_payload = messaging.Notification(
        title=notification_title,
        body=notification_body
    )
    message = messaging.Message(
        notification=notification_payload,
        token=fcm_token
    )

    print(f"Enviando mensaje a {fcm_token}...")
    response = messaging.send(message)
    print(f"Mensaje enviado con éxito: {response}")

except Exception as e:
    print(f"Error al enviar el mensaje: {e}")