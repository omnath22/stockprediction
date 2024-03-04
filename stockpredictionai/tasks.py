from email.message import EmailMessage
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

# @shared_task
# def send_weekly():
#     subject = 'Hello from Django'
#     body = 'This is a test email sent from Django.'
#     from_email = 'omnathgupta11@gmail.com'
#     to_email = 'og501110@gmail.com'

#     message = EmailMessage(subject, body, from_email, [to_email])
#     message.send()

#     print("Email sent successfully!")
from celery.schedules import crontab
from celery import app

@app.task(
run_every=(crontab(hour=3, minute=34)), #runs exactly at 3:34am every day
name="Dispatch_scheduled_mail",
reject_on_worker_lost=True,
ignore_result=True)
def send_weekly():
    subject = 'Hello from Django'
    body = 'This is a test email sent from Django.'
    from_email = 'omnathgupta11@gmail.com'
    to_email = 'og501110@gmail.com'

    message = EmailMessage(subject, body, from_email, [to_email])
    message.send()

    print("Email sent successfully!")
    