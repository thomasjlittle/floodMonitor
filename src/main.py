import logging
import os
from dotenv import load_dotenv

from scrape_web import scrape_web
from process_data import process_data
from make_report import make_report
from send_email import send_email

# Load environment variables from .env file
load_dotenv()  

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a' 
)
logger = logging.getLogger()

# Load env vars
try:
    stage_threshold = float(os.environ["STAGE_THRESHOLD"])
except KeyError:
    logger.error("No stage threshold set... oh dang...")
    raise
except ValueError:
    logger.error("Invalid stage threshold value. It must be a float.")
    raise

url = os.getenv("URL")
if not url:
    logger.error("No url set... oh shoot...")

subject = os.getenv("SUBJECT","You've got Mail! >:)")
sender_email = os.getenv("SENDERS_EMAIL")
receiver_email = os.getenv("RECEIVERS_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

if not all([sender_email, receiver_email, smtp_server, smtp_port, username, password]):
    logger.error("Ensure all environmental variables are configured correctly")
    raise Exception("Ensure all environmental variables are configured correctly")

# Thcrape the Web
data = scrape_web(url, logger)

# Protheth the resulth
flood_points = process_data(data, stage_threshold, logger)

# Make the report
report = make_report(flood_points, stage_threshold, url, logger)

# Send the email
send_email(
    subject,
    html_body=report,
    from_addr=sender_email,
    to_addr=receiver_email,
    smtp_server=smtp_server,
    smtp_port=smtp_port,
    username=username,
    password=password,
    logger=logger
)

print(report)