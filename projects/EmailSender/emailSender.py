# Author - Killian O'Connor
# Date - 06/08/25
# Description - Allows the user to send emails - program extended from TechWithTim - can now choose message, body, receiver and send images

import smtplib
import ssl
from email.message import EmailMessage
import mimetypes
import os

SENDER = "killianscodetester@gmail.com"
PASS = "ryoa bqfd qkwk pegy"  # app password for Gmail

# getting user input 
receiver = input("Enter the receiver's email: ")
subject = input("Enter subject: ")
body = input("Enter email body: ")
add_image = input("Do you want to attach an image? (y/n): ").lower() # allows Y or y

message = EmailMessage()
message["From"] = SENDER
message["To"] = receiver
message["Subject"] = subject

# HTML email 
html = f"""
<html>
    <body>
        <h1>{subject}</h1>
        <p>{body}</p>
    </body>
</html>
"""
message.add_alternative(html, subtype="html")

#  adding the image if the user says 
if add_image == "y":
    path = input("enter the image file path: ")
    if os.path.exists(path):
        with open(path, "rb") as img:
            file_data = img.read()
            maintype, subtype = mimetypes.guess_type(path)[0].split("/")
            message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))
    else:
        print("image not found, skipping")

# send email 
context = ssl.create_default_context()

print("Sending Email...")

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(SENDER, PASS)
    server.send_message(message)

print("Email sent.")
