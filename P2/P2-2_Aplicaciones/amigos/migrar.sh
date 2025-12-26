#!/bin/bash

# 1. Definimos la variable con el mensaje de la migración
MENSAJE="Mensaje migrar"

# 2. Establecemos la variable de entorno para que Flask sepa dónde está la app
export FLASK_APP=lanzar.py

# 3. Generamos el archivo de migración (detecta el cambio en models.py)
echo "Generando migración con el mensaje: $MENSAJE"
flask db migrate -m "$MENSAJE"

# 4. Aplicamos los cambios a la base de datos
echo "Aplicando cambios a la base de datos..."
flask db upgrade

echo "¡Proceso terminado!"