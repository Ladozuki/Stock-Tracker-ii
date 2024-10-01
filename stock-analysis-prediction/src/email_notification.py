import smtplib 
from email.mine.text import MIMEText

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = ''
    msg['To'] = to_email

    with smtplib.SMTP('') as server:
        server.login('', '')
        server.send_message(msg)