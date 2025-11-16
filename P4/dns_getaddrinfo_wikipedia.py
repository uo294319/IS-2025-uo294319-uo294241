import socket

host = "en.wikipedia.org"
service = "www"   # equivalente al puerto 80

info = socket.getaddrinfo(host, service)
print(f"Información de {host} para el servicio {service}:\n")
for entry in info:
    family, socktype, proto, canonname, sockaddr = entry
    print(f"Family: {family}, Socktype: {socktype}, Proto: {proto}, Canonname: {canonname}, Sockaddr: {sockaddr}")

ipv4_info = next(e for e in info if e[0] == socket.AF_INET)

family, socktype, proto, canonname, sockaddr = ipv4_info
print(f"Usando IPv4: {sockaddr}")

# Crear el socket y conectarse
with socket.socket(family, socktype, proto) as s:
    s.connect(sockaddr)
    print("Conectado correctamente por IPv4.")

    # ---------------------------------------------------
    # 3. Enviar petición HTTP al servidor
    # ---------------------------------------------------
    http_request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    s.sendall(http_request.encode())

    # ---------------------------------------------------
    # 4. Recibir y mostrar la respuesta
    # ---------------------------------------------------
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data

    print("\n--- Respuesta del servidor (IPv4) ---\n")
    print(response.decode(errors="ignore"))