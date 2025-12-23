# PL6

## 2.2.1 Instalación y nombre
1. `get-image-prosody.sh`
2. `docker run --rm -d --name prosody unclev/prosody-docker-extended:0.10`
3. `mkdir etc data`
4. `docker cp prosody:/etc/prosody etc`
5. En `prosody/etc/prosody/prosody.cfg.lua` cambia el atributo `VirtualHost` con nombre. 

## 2.2.2
`lanza-prosody.sh`

## 2.2.3 Creacion certs
```bash
docker exec -it prosody bash

prosodyctl cert generate <nombre>

exit
```
El `nombre` está en `prosody/etc/prosody/prosody.cfg.lua` en el atributo `VirtualHost`
## 2.2.4 Alta de usuarios
```bash
docker exec -it prosody bash

prosodyctl adduser manolo@ingservXX
prosodyctl adduser ramon@ingservXX

exit
```
## 5 Uso del bot
(Modificar constantes en codigo)
### Añadir usuario bot
```bash
docker exec -it prosody bash
prosodyctl adduser bot@ingservXX
exit
```
Luego ejecutar `export CLAVEBOT=XXXXXX` con la clave del bot.