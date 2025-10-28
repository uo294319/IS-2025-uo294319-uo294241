#!/bin/bash
docker run -d --rm --network pruebas    --name nginx -p 81:81    -v $(pwd)/html2:/usr/share/nginx/html2    -v $(pwd)/sitios_nginx:/etc/nginx/conf.d nginx
