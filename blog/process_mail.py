from email.message import EmailMessage
import smtplib
from django.conf import settings


def send_my_mail(sub, msg_from, msg_to, msg_content):
    mess = EmailMessage()

    mess['Subject'] = sub
    mess['From'] = msg_from
    mess['To'] = msg_to
    mess.set_content(f" \n msg_content")

    html_message = f"""
            <!Doctype html>
            <html>
            <body>
            <h4 style='font-style:italic;'>{sub}</h4>
            <br>
            <p style='color:SlateGray;'>  {msg_content} </p>
            </body>
            </html>
            </html>
            """

    mess.add_alternative(html_message, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(mess)
