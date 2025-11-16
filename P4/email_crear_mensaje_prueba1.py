import email.message, email.policy, email.utils


mensaje = email.message.EmailMessage()
mensaje['To'] = 'Ignacio Pujades <uo294241@uniovi.es>'
mensaje['From'] = 'Ángel Arróspide <uo294319@uniovi.es>'
mensaje['Subject'] = 'Hola'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Sí soy yo. Soy el fantasma de las navidades pasadas.")

binario = mensaje.as_bytes()
print()
print(binario.decode("utf-8"))