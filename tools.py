import smtplib
from email.mime.text import MIMEText
import config


def send_email(to, subject, body, sender=None):

    if sender is None:
        sender_email = config.mail_username
    else:
        sender_email = sender
        
    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = to
    msg["Subject"] = subject 

    with smtplib.SMTP_SSL(host=config.mail_host, port=config.mail_port) as server:
        server.login(user=config.mail_username, password=config.mail_password)
        server.sendmail(sender_email, to, msg.as_string())
        server.quit()