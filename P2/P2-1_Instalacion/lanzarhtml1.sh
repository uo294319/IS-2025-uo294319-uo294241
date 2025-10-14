#!/bin/bash
docker run -d --rm --network pruebas    --name nginx -p 80:80    -v $(pwd)/html2:/usr/share/nginx/html2    -v $(pwd)/sitios_nginx:/etc/nginx/conf.d nginx
