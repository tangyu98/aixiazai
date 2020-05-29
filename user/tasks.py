from django.core.mail import EmailMessage
from celery import app

@app.shared_task
def send_mail(subject, body, to, subtype="html"):
    message = EmailMessage(subject=subject, body=body, to=to)
    message.content_subtype = subtype
    message.send()
