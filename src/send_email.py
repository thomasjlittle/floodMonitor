import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(
        subject: str, 
        html_body: str, 
        from_addr: str, 
        to_addr: str, 
        smtp_server: str, 
        smtp_port: int, 
        username: str, 
        password: str,
        logger: logging.Logger = None
    ):
    if logger is None:
        logger = logging.getLogger(__name__)
    
    # Create a MIME message
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    # Attach the HTML part of the email
    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(username, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error("Failed to send email: %s", e)
