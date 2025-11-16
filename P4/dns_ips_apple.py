import dns.resolver

respuesta = dns.resolver.query('apple.com')

for ip in respuesta:
    print(ip.address)
