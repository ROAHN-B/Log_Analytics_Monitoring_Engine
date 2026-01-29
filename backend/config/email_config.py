import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

EMAIL="rohanbelsare113@gmail.com"
PASSWORD="auex mhqe squb szvs"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=465

def send_mail(to_mail:str,anomaly:dict):
    subject="Log anomaly detected"
    body=f"""
        Anomaly detected in system logs
        time window: {anomaly['timestamp']}
        Error count: {anomaly['error_count']}
        Z score: {anomaly['z_score']}
        Please review log data.

        Regards,
        Rohan Belsare.
"""
    msg=EmailMessage()
    msg["subject"]=subject
    msg["from"]=EMAIL
    msg["to"]=to_mail
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT) as server:
        server.login(EMAIL,PASSWORD)
        server.send_message(msg) 