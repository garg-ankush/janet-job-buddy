import urllib.parse
import smtplib
import pygame
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

def send_email_from_json(json_file):
    # Load email information from JSON file
    with open(json_file) as f:
        email_data = json.load(f)

    sender_email = email_data.get('sender_email', '')
    recipient_email = email_data.get('recipient_email', '')
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')

    # Create a new SES resource
    ses = boto3.client('ses', region_name='us-west-2')  # Specify your desired AWS region

    # Send the email
    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )

        logging.info("Email sent successfully!")
        logging.info("Message ID: %s", response['MessageId'])
    except Exception as e:
        logging.error("Failed to send email. Error: %s", str(e))

def generate_email_json(sender_email, recipient_email, subject, body, json_file_path):
    email_data = {
        "sender_email": sender_email,
        "recipient_email": recipient_email,
        "subject": subject,
        "body": body
    }

    with open(json_file_path, 'w') as f:
        json.dump(email_data, f, indent=4)

def play_audio_file(file_path):
    # Initialize Pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait until audio finishes playing
    while pygame.mixer.music.get_busy():
        continue
