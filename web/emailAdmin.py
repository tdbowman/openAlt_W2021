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


def emailAdmin(pw):

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    SMTP_USERNAME = 'openaltteam@gmail.com'
    SMTP_PASSWORD = 'bowmanwsu'

    msg = MIMEMultipart()
    msg['From'] = 'OpenAlt v2.0'
    msg['To'] = 'tabishshaikh97@gmail.com'
    msg['Subject'] = 'Admin Login'



    body = """\
    <html>
    <head></head>
    <body>
        <h3 style="font-weight:normal;"> Your password is: <b>""" + str(pw) + """</b></h3>
    </body>
    </html>
    """

    body_part = MIMEText(body, 'html')
    msg.attach(body_part)


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
