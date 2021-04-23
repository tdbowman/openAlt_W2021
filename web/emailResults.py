# Author: Darpan (whole file)
"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import smtplib for the actual sending function
import smtplib
import ssl

# Import the email modules we'll need
from email.message import EmailMessage

# Import for attachments
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication as ma
from email.mime.text import MIMEText

import uploadDOI
import uploadAuthor
import uploadUni
import os

## For SMTP Info -> https://support.google.com/mail/answer/7126229?hl=en


def emailResults(zipPath, recipient, type):
    zipPath = zipPath

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    SMTP_USERNAME = 'openaltteam@gmail.com'
    SMTP_PASSWORD = 'bowmanwsu'

    msg = MIMEMultipart()
    msg['From'] = 'OpenAlt v2.0'
    msg['To'] = recipient

    if type == 'doi':
        metadataStats = uploadDOI.getMetadataStats()
        eventStats = uploadDOI.getEventStats()
        msg['Subject'] = 'OpenAlt v2.0: Your DOI Results Are Ready!'
        body = 'Thank You for using OpenAlt! You will find your results attached to this email.\n\n\nRESULTS:\n' + metadataStats + '\n' + eventStats
              
    if type == 'author':
        authorStats = uploadAuthor.getStats()
        msg['Subject'] = 'OpenAlt v2.0: Your Author Results Are Ready!'
        body = 'Thank You for using OpenAlt! You will find your results attached to this email.\n\n\n\n' + authorStats
    
    if type == 'uni':
        uniStats = uploadUni.getStats()
        msg['Subject'] = 'OpenAlt v2.0: Your University Results Are Ready!'
        body = 'Thank You for using OpenAlt! You will find your results attached to this email.\n\n\n\n' + uniStats


    body_part = MIMEText(body, 'plain')
    msg.attach (body_part)

    with open(zipPath, 'rb') as file:
        msg.attach(ma(file.read(), Name = os.path.basename(zipPath)))


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

    os.remove(zipPath)