import logging
import datetime
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

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
    low_stage_threshold = float(os.environ["LOW_STAGE_THRESHOLD"])
    high_stage_threshold = float(os.environ["HIGH_STAGE_THRESHOLD"])
except KeyError:
    logger.error("Stage thresholds are not set... oh dang...")
    raise
except ValueError:
    logger.error("Invalid stage threshold value. It must be a float.")
    raise

# Set up the URL
base_url = os.getenv("URL")
station = os.getenv("STATION")
url = f"{base_url}{station}"
if not url:
    logger.error("No url set... oh shoot...")

# Set up the email info
subject = os.getenv("SUBJECT","You've got Mail! >:)")
sender_email = os.getenv("SENDERS_EMAIL")
receiver_emails = os.getenv("RECEIVERS_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

if not all([sender_email, receiver_emails, smtp_server, smtp_port, username, password]):
    logger.error("Ensure all environmental variables are configured correctly")
    raise Exception("Ensure all environmental variables are configured correctly")

# Thcrape the Web
data = scrape_web(url, logger)

# Protheth the resulth
points_over_low_threshold, points_over_high_threshold = process_data(data, low_stage_threshold, high_stage_threshold, logger)

# Make the report
utc_time = datetime.timezone.utc
current_time = datetime.datetime.now(datetime.timezone.utc)
current_hour = current_time.hour
report = None

if points_over_high_threshold:
    warning_level = os.getenv("HIGH_WARNING_LEVEL", "HIGH")
    report = make_report(points_over_low_threshold, points_over_high_threshold, low_stage_threshold, high_stage_threshold, url, logger)
elif current_hour in [13, 1]:
    if points_over_low_threshold:
        warning_level = os.getenv("MEDIUM_WARNING_LEVEL", "MEDIUM")
    else:
        warning_level = os.getenv("LOW_WARNING_LEVEL", "LOW")
    report = make_report(points_over_low_threshold, points_over_high_threshold, low_stage_threshold, high_stage_threshold, url, logger)

# Send the email
if report:
    send_email(
        subject,
        station,
        warning_level,
        html_body=report,
        from_addr=sender_email,
        to_addrs=receiver_emails.split(","),
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password,
        logger=logger
    )
