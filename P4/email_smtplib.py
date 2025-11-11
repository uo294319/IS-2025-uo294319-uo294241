import getpass
import os
import smtplib
import email.message, email.policy, email.utils

server = 'smtp.gmail.com'
port = 587
fromaddr = 'test.si2024.pl51@gmail.com'
toaddr   = 'uo294319@uniovi.es'
subject = 'Hola'
data = 'Soy el fantasma de las navidades pasadas.'

if __name__ == '__main__':
    mensaje=email.message.EmailMessage()
    mensaje['To'] = '<{}>'.format(toaddr)
    mensaje['From'] = '<{}>'.format(fromaddr)
    mensaje['Subject'] = '{}'.format(subject)
    mensaje['Date'] = email.utils.formatdate(localtime=True)
    mensaje['Message-ID'] = email.utils.make_msgid()
    mensaje.set_content("{}\r\n. \r\n".format(data))

    s = smtplib.SMTP(server, port)
    s.set_debuglevel(1)
    s.starttls()
    
    try:
        # Login
        #username=input("Usuario: ")
        username = fromaddr
        password = os.getenv("PSSWD")

        s.login(username,password)

        # Send
        s.sendmail(fromaddr, toaddr, mensaje.as_bytes())
    except AttributeError:
        print('Crea la variable con EXPORT PASSWD="tu_contraseña"')
    except smtplib.SMTPAuthenticationError:
        print("Invalid Credentials")
    
    s.close()

