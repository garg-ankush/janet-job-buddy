import os
import urllib.parse
import pygame
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import boto3
from botocore.exceptions import NoCredentialsError


def generate_job_search_link(keywords):
    base_url = "https://www.indeed.com/jobs"

    #encoded_keywords = urllib.parse.quote(keywords)

    #query_params = {
    #    "q": encoded_keywords,
    #}
    print(keywords) 
    search_url = base_url + "?=" + "+".join(keywords)#urllib.parse.urlencode(query_params)

    return search_url


def send_email_from_json_attachment(json_file_path, attachment_file=None):
    # Load email information from JSON file
    with open(json_file_path) as f:
        email_data = json.load(f)

    sender_email = email_data.get('sender_email', '')
    recipient_email = email_data.get('recipient_email', '')
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')

    # Create a new SES resource
    ses = boto3.client(
        'ses',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET")
    )  # Specify your desired AWS region

    # Create a multipart/mixed email and attach the text and document parts
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Attach the email body as a plain text part
    body_text = MIMEText(body, 'plain')
    msg.attach(body_text)

    # Attach the document as an attachment if provided
    if attachment_file:
        with open(attachment_file, 'rb') as f:
            attachment = MIMEApplication(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_file)
        msg.attach(attachment)

    try:
        # Send the email
        ses.send_raw_email(
            Source=sender_email,
            Destinations=[recipient_email],
            RawMessage={
                'Data': msg.as_string()
            }
        )
        print("Email sent successfully!")

    except NoCredentialsError:
        print("Failed to send email. AWS credentials not found.")
    except Exception as e:
        print("Failed to send email. Error: %s", str(e))


def generate_email_json(sender_email, recipient_email, subject, body_file, search_url, json_file_path):
    with open(body_file, 'r') as f:
        body = f.read()
        body = body + "\n" + f"Here is the link for finding jobs: {search_url}"

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
