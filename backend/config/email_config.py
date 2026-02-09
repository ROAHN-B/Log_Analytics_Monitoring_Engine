import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

EMAIL="rohanbelsare113@gmail.com"
PASSWORD="auex mhqe squb szvs"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=465

def send_mail(to_mail:str,anomaly:dict):
    subject=f"[ALERT] Log Anomaly Detected"
    body=f"""
        ⚠️ Automated System Alert: Log Anomaly Detected

    An unusual spike in system errors has been identified by the monitoring script.

    --- Details ---
    Timestamp Window : {anomaly['timestamp']}
    Error Count      : {anomaly['error_count']}
    Z-Score          : {anomaly['z_score']}

    --- Action Required ---
    Please review the log management dashboard or SSH into the production server 
    to investigate the root cause.

    This is an automated message.
    Regards,
    Rohan Belsare
    """
    msg=EmailMessage()
    msg["subject"]=subject
    msg["from"]=EMAIL
    msg["to"]=to_mail
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT) as server:
        server.login(EMAIL,PASSWORD)
        server.send_message(msg) 