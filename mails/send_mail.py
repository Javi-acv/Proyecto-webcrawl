import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo():
    try:
        #Mail settings
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login('proyectowebcrawler@gmail.com','xieg alws eejs ixzf')
        
        mensaje= MIMEMultipart()
        mensaje['From']='WebCrawler'
        mensaje['To']='alvaritodavilag0331@gmail.com'
        mensaje['Subject']='Resultados de búsqueda'
        
        #read json file
        with open('crawl/test.json','r',encoding='utf-8') as f:
            contenido=json.load(f)
        
        #body mail
        contenido_correo="""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h2>Listado de conciertos</h2>
            <table>
                <tr>
                    <th>Artista</th>
                    <th>Lugar</th>
                    <th>Ciudad</th>
                    <th>Fecha</th>
                    <th>Enlace</th>
                </tr>
        """

        for concierto in contenido:
            contenido_correo += f"""
                <tr>
                    <td>{concierto['Artista']}</td>
                    <td>{concierto['Lugar']}</td>
                    <td>{concierto['Ciudad']}</td>
                    <td>{concierto['Fecha']}</td>
                    <td><a href="{concierto['Enlace']}">Ver detalle</a></td>
                </tr>
            """

        contenido_correo += """
            </table>
        </body>
        </html>
        """

        mensaje.attach(MIMEText(contenido_correo,'html'))
        #send mail
        server.sendmail('proyectowebcrawler@gmail.com','alvaritodavilag0331@gmail.com',mensaje.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()

#test send mail
enviar_correo()