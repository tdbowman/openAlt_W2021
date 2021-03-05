# Author: Darpan (whole file)

# Import smtplib for the actual sending function
import smtplib
import ssl

# Import the email modules we'll need
from email.message import EmailMessage

# Import for attachments
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication as ma
from email.mime.text import MIMEText


## For SMTP Info -> https://support.google.com/mail/answer/7126229?hl=en


def emailError(recipient, type):
    
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    SMTP_USERNAME = 'openaltteam@gmail.com'
    SMTP_PASSWORD = 'bowmanwsu'

    msg = MIMEMultipart()
    msg['From'] = 'OpenAlt v2.0'
    msg['To'] = recipient

    if type == 'doi':
        msg['Subject'] = 'OpenAlt v2.0: Error finding DOI Results'
        body = 'Thank You for using OpenAlt! We are very sorry but we seem to have ran into an issue on our end and were not able to process your search. Please try again in a couple of minutes.'
              
    if type == 'author':
        msg['Subject'] = 'OpenAlt v2.0: Error finding Author Results'
        body = 'Thank You for using OpenAlt! We are very sorry but we seem to have ran into an issue on our end and were not able to process your search. Please try again in a couple of minutes.'
    
    if type == 'uni':
        msg['Subject'] = 'OpenAlt v2.0: Error finding Author Results'
        body = 'Thank You for using OpenAlt! We are very sorry but we seem to have ran into an issue on our end and were not able to process your search. Please try again in a couple of minutes.'

    body_part = MIMEText(body, 'plain')
    msg.attach (body_part)

    
    # Create SMTP object
    smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    # Login to the server
    print("\nLogging in...")
    smtp_obj.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Convert the message to a string and send it
    print("Email sending...")
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()

    print("Email sent!")

    #os.remove(zipPath)