from email.message import EmailMessage
import smtplib
from django.conf import settings
from django.template.loader import get_template


def send_my_mail(subject, email_from, email_to, context, html_template):
    html_temp_path = html_template
    context = context
    email_html_template = get_template(html_temp_path).render(context)
    mess = EmailMessage()

    mess['Subject'] = subject
    mess['From'] = email_from
    mess['To'] = email_to
    mess.set_content = email_html_template

    html_message = email_html_template

    mess.add_alternative(html_message, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(mess)
