import dns.resolver

respuesta = dns.resolver.query('en.wikipedia.org')
print(respuesta[0].address)
print()
print(respuesta.response)
print()
print(respuesta.response.to_wire())
