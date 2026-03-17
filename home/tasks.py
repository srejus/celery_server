# tasks.py
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from .models import EmailLog

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,),
             retry_backoff=30, retry_kwargs={"max_retries": 5})
def call_url_task(self, url, method="GET", payload=None, headers=None, timeout=15):
    """
    Calls a given URL.

    Parameters
    ----------
    url : str
    method : GET | POST
    payload : dict (optional JSON body)
    headers : dict (optional headers)
    timeout : request timeout
    """

    payload = payload or {}
    headers = headers or {}

    if method.upper() == "POST":
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    else:
        response = requests.get(url, headers=headers, timeout=timeout)

    return {
        "status_code": response.status_code,
        "response": response.text[:500]
    }


@shared_task(bind=True)
def send_email_task(self,to_email, subject, html_content,
                        from_email,email_password):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_sender = 'Orca'

    msg = MIMEMultipart()
    msg['From'] = f"{from_sender} <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(from_email, email_password)
            server.sendmail(from_email, to_email, msg.as_string())
        logger.info("Email sent successfully!")
        EmailLog.objects.create(from_email=from_email,to_email=to_email,subject=subject,data="Email Sent Successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        EmailLog.objects.create(from_email=from_email,to_email=to_email,subject=subject,data=f"Error sending email: {e}")