from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import smtplib
from config import *


def send_email(content, subject, receiver_email, cc_email=None, sender_email='sabahraporu@skoda.com.tr',login=None,password=None):
    message = MIMEText(content, "html")
    message["Subject"] = subject
    message["From"] = sender_email

    # Ensure receiver_email and cc_email are both lists
    if not isinstance(receiver_email, list):
        receiver_email = [receiver_email]
    if cc_email and not isinstance(cc_email, list):
        cc_email = [cc_email]

    # Construct the recipients lists
    to_recipients = receiver_email
    cc_recipients = cc_email if cc_email else []

    message["To"] = ", ".join(to_recipients)
    message["Cc"] = ", ".join(cc_recipients)

    recipients = to_recipients + cc_recipients


    if sender_email=="skodasatis@skoda.com.tr":
        server = smtplib.SMTP("mail.yuceauto.com.tr",465)
        server.starttls()
        server.login(login, password)
    else:
        server = smtplib.SMTP("mail.yuceauto.com.tr")
        server.starttls()
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()

def send_email_2(sender_email, mail_password, subject, content, receiver_email, cc_email=None, bcc_email=None, attachment=None):
    password = mail_password

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    
    if not isinstance(receiver_email, list):
        receiver_email = [receiver_email]
    if cc_email and not isinstance(cc_email, list):
        cc_email = [cc_email]
    if bcc_email and not isinstance(bcc_email, list):
        bcc_email = [bcc_email]

    to_recipients = receiver_email
    cc_recipients = cc_email if cc_email else []
    bcc_recipients = bcc_email if bcc_email else []

    if message["To"] != None:
        message["To"] = ", ".join(to_recipients)
    message["Cc"] = ", ".join(cc_recipients)
    message["Bcc"] = ", ".join(bcc_recipients)

    recipients = to_recipients + cc_recipients + bcc_recipients

    message.attach(MIMEText(content, "html"))

    if attachment:
        if not isinstance(attachment, list):
            attachment = [attachment]
        
        for file_path in attachment:
            if os.path.exists(file_path):
                with open(file_path, "rb") as attachment_file:
                    part = MIMEApplication(attachment_file.read(), Name=os.path.basename(file_path))

                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                message.attach(part)

    server = smtplib.SMTP("mail.yuceauto.com.tr", 465)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()