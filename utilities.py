import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


def generate_job_search_link(keywords):
    base_url = "https://www.indeed.com/jobs"

    encoded_keywords = urllib.parse.quote(keywords)

    query_params = {
        "q": encoded_keywords,
    }

    search_url = base_url + "?" + urllib.parse.urlencode(query_params)

    return search_url

def send_email(sender_email, sender_password, recipient_email, subject, body):
    # SMTP server configuration (example for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create a secure connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the sender's email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

        # Close the connection
        server.quit()

        # Log success message to a file
        logging.basicConfig(filename='email_log.txt', level=logging.INFO)
        logging.info("Email sent successfully!")
    except smtplib.SMTPException as e:
        # Log failure message to a file
        logging.basicConfig(filename='email_log.txt', level=logging.ERROR)
        logging.error("Failed to send email. Error: %s", str(e))
