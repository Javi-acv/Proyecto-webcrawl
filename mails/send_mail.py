import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo():
    #Configurar correo 
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('proyectowebcrawler@gmail.com','xieg alws eejs ixzf')
    