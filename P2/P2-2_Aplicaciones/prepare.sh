#!/bin/bash

# Crear la red 'pruebas'. Si ya existe, no muestra error y continua.
docker network create pruebas 2>/dev/null || true

# Descargar las imágenes
echo "Descargando imágenes..."
docker pull python:3.7
docker pull nginx:latest
docker pull mariadb:latest

echo "--- Entorno preparado ---"