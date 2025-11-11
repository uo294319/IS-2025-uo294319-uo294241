import dns.resolver

respuesta = dns.resolver.query("gmail.com", "MX")

for item in respuesta:
    item_ip =[j.address for j in dns.resolver.query(item.exchange)]
    print(item_ip, item.exchange, sep="\t")

    
