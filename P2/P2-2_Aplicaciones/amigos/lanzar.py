from app import create_app
import os

# Usarlo para instanciar la aplicacion
modo = os.getenv("DEPLOYMENT_MODE", "production")
app = create_app(modo)